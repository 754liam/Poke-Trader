# Main application routes for dashboard, card search, trading, and admin functionality
# Flask, Flask-Login, SQLAlchemy, requests, zoneinfo

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user, logout_user
from app.models import User, Card, CollectionItem, Trade, OfferedCard, RequestedCard, TradeStatus
from app import db
from app.precached_pokemon import get_precached_cards
import requests
import os
import time
import json
import hashlib
import random
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

bp = Blueprint('main', __name__)



ADMIN_USERS = set(
    user.strip().lower()
    for user in os.environ.get('ADMIN_USERS', '').split(',')
    if user.strip()
)

def is_admin():

    if not current_user.is_authenticated:
        return False

    return (
        current_user.email.lower() in ADMIN_USERS or
        current_user.username.lower() in ADMIN_USERS
    )

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function



if os.environ.get('VERCEL'):
    default_cache_root = Path('/tmp/poketrader_cache')
else:
    default_cache_root = Path('cache')

CACHE_DIR = Path(os.environ.get('POKETRADER_CACHE_DIR', default_cache_root))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DURATION = timedelta(hours=24)


INSTANT_POKEMON = ['Pikachu', 'Charizard', 'Mewtwo', 'Meowscarada']


APP_TIMEZONE = ZoneInfo('UTC')


COMMON_POKEMON = INSTANT_POKEMON + [
    'Blastoise', 'Venusaur', 'Mew', 'Lucario', 'Garchomp', 'Gengar',
    'Snorlax', 'Dragonite', 'Tyranitar', 'Rayquaza', 'Groudon', 'Kyogre',
    'Dialga', 'Palkia', 'Giratina', 'Arceus', 'Zekrom', 'Reshiram',
    'Kyurem', 'Xerneas', 'Yveltal', 'Zygarde', 'Solgaleo', 'Lunala',
    'Necrozma', 'Eternatus', 'Zacian', 'Zamazenta', 'Urshifu', 'Calyrex',
    'Koraidon', 'Miraidon', 'Ogerpon'
]


_api_session = None


_last_api_call_time = None
_min_api_delay = 1.0

def get_api_session():

    global _api_session
    if _api_session is None:
        _api_session = requests.Session()

        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=0
        )
        _api_session.mount('https://', adapter)

        _api_session.headers.update({'Accept-Encoding': 'gzip, deflate'})
    return _api_session

def _rate_limit_api_call():

    global _last_api_call_time
    if _last_api_call_time is not None:
        time_since_last = time.time() - _last_api_call_time
        if time_since_last < _min_api_delay:
            sleep_time = _min_api_delay - time_since_last
            time.sleep(sleep_time)
    _last_api_call_time = time.time()

def get_cache_path(query):

    cache_key = hashlib.md5(query.lower().encode()).hexdigest()
    return CACHE_DIR / f"{cache_key}.json"

def load_from_cache(query):

    cache_file = get_cache_path(query)
    if not cache_file.exists():
        return None

    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)
            cache_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cache_time < CACHE_DURATION:
                return data['cards']
    except (json.JSONDecodeError, KeyError, ValueError):

        cache_file.unlink()
    return None

def save_to_cache(query, cards):

    cache_file = get_cache_path(query)
    try:
        with open(cache_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'cards': cards
            }, f)
    except Exception:

        pass

def _stable_price_seed(name, set_name=None):

    base = (name or 'unknown').lower()
    if set_name:
        base += f"|{set_name.lower()}"
    digest = hashlib.sha256(base.encode('utf-8')).hexdigest()
    return (int(digest[:12], 16) % 1000) + 1

def initialize_card_price(card):

    today = datetime.now(APP_TIMEZONE).date()
    price_changed = False
    new_price = card.price


    if card.price is None or card.last_price_update != today:

        base_price = _stable_price_seed(card.name, card.set_name)

        if card.price is None:

            new_price = base_price
        else:

            variation = random.randint(-20, 20)
            new_price = int(base_price * (1 + variation / 100))


        new_price = max(1, min(1000, new_price))

        card.price = new_price
        card.last_price_update = today
        price_changed = True

    if price_changed:

        for owner_item in card.owners:
            owner_item.current_price = calculate_condition_price(new_price, owner_item.condition)
        db.session.commit()

    return card.price

def update_daily_prices():

    today = datetime.now(APP_TIMEZONE).date()
    cards = Card.query.filter(
        (Card.last_price_update != today) | (Card.last_price_update.is_(None))
    ).all()

    updated_count = 0
    for card in cards:

        fluctuation = random.uniform(-0.15, 0.15)
        new_price = int(card.price * (1 + fluctuation))


        new_price = max(1, min(1000, new_price))

        card.price = new_price
        card.last_price_update = today
        updated_count += 1

    if updated_count > 0:
        db.session.commit()


    return updated_count

def get_time_until_next_price_update():

    now = datetime.now(APP_TIMEZONE)

    next_update = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_remaining = next_update - now

    total_seconds = int(time_remaining.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return {
        'formatted': f"{hours}h {minutes}m {seconds}s",
        'total_seconds': total_seconds,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }

@bp.route('/')
def index():

    return render_template('index.html', title='Home')

def calculate_condition_price(base_price, condition):

    condition_multipliers = {
        'Near Mint': 1.0,
        'Lightly Played': 0.8,
        'Moderately Played': 0.64,
        'Heavily Played': 0.512,
        'Damaged': 0.4096
    }
    multiplier = condition_multipliers.get(condition or 'Near Mint', 1.0)
    return max(1, int(base_price * multiplier))

@bp.route('/dashboard')
@login_required
def dashboard():


    db.session.refresh(current_user)

    collection = CollectionItem.query.filter_by(user_id=current_user.id).all()


    for item in collection:
        initialize_card_price(item.card_info)


    collection_with_prices = []
    prices_updated = False
    for item in collection:
        base_price = item.card_info.price
        stored_current_price = item.current_price or 0
        if stored_current_price <= 0:
            stored_current_price = calculate_condition_price(base_price, item.condition)
            item.current_price = stored_current_price
            prices_updated = True
        collection_with_prices.append({
            'item': item,
            'display_price': stored_current_price,
            'base_price': base_price,
            'purchase_price': item.purchase_price or stored_current_price
        })

    if prices_updated:
        db.session.commit()

    time_until_update = get_time_until_next_price_update()
    return render_template('dashboard.html',
                         title='Dashboard',
                         collection=collection_with_prices,
                         balance=current_user.balance,
                         time_until_update=time_until_update)

@bp.route('/search/users')
@login_required
def search_users():

    query = request.args.get('q', '').strip()
    users = []
    current_user_id = getattr(current_user, 'id', None)

    if query:


        query_stmt = User.query.filter(User.username.ilike(f'%{query}%'))
        if current_user_id is not None:
            query_stmt = query_stmt.filter(User.id != current_user_id)
        users = query_stmt.limit(20).all()


    if current_user_id is not None:
        users = [user for user in users if user.id != current_user_id]

    return render_template('search_users.html', title='Search Users', users=users, query=query)

@bp.route('/pokemon')
@login_required
def pokemon_list():


    db_pokemon = db.session.query(Card.name).distinct().order_by(Card.name).all()
    db_pokemon_names = [row[0] for row in db_pokemon]


    all_pokemon = sorted(list(set(COMMON_POKEMON + db_pokemon_names)))


    pokemon_by_letter = {}
    for pokemon in all_pokemon:
        first_letter = pokemon[0].upper()
        if first_letter not in pokemon_by_letter:
            pokemon_by_letter[first_letter] = []
        pokemon_by_letter[first_letter].append(pokemon)

    return render_template('pokemon_list.html',
                         title='Available Pokemon',
                         pokemon_by_letter=pokemon_by_letter,
                         total_count=len(all_pokemon))

@bp.route('/user/<username>')
@login_required
def view_user(username):

    user = User.query.filter_by(username=username).first_or_404()


    tradeable_cards = CollectionItem.query.filter_by(
        user_id=user.id
    ).all()

    return render_template('user_profile.html',
                         title=f"{user.username}'s Profile",
                         user=user,
                         tradeable_cards=tradeable_cards)

def _filter_cards_by_name(cards, search_term):

    search_lower = search_term.lower()
    filtered = []
    for card in cards:
        if isinstance(card, dict):
            card_name = card.get('name', '').lower()


            if card_name and card_name.startswith(search_lower):
                filtered.append(card)
    return filtered

def _deduplicate_cards(cards):

    seen = {}
    for card in cards:
        if isinstance(card, dict):
            card_name = card.get('name', '')
            set_name = card.get('set', {}).get('name', '') if isinstance(card.get('set'), dict) else ''
            key = f"{card_name}|{set_name}"



            if key not in seen:
                seen[key] = card
            else:

                existing = seen[key]
                existing_has_image = existing.get('images', {}).get('small')
                current_has_image = card.get('images', {}).get('small')
                if current_has_image and not existing_has_image:
                    seen[key] = card

    return list(seen.values())


def _perform_card_search(query):

    cards = []
    error = None
    from_cache = False
    api_failed = False

    if not query or len(query) < 2:
        return cards, error, from_cache, api_failed


    normalized_query = query.strip().lower()
    search_query = query.strip()


    precached = get_precached_cards(normalized_query)
    if precached is not None and len(precached) > 0:
        cards = precached
        from_cache = True
        return cards, error, from_cache, api_failed


    cached_cards = load_from_cache(normalized_query)
    if cached_cards is not None:
        cards = cached_cards
        from_cache = True

        return cards, error, from_cache, api_failed



    _rate_limit_api_call()

    api_key = os.environ.get('POKEMON_TCG_API_KEY')
    headers = {'X-Api-Key': api_key} if api_key else {}
    session = get_api_session()




    search_for_api = ' '.join(word.capitalize() for word in search_query.split())
    is_simple_name = " " not in search_query and search_query.isalpha()


    timeout_seconds = 30

    try:

        if is_simple_name:

            exact_query = f'name:"{search_for_api}"'
            response = session.get(
                'https://api.pokemontcg.io/v2/cards',
                params={
                    'q': exact_query,
                    'pageSize': 20,
                    'select': 'id,name,set,images',
                    'orderBy': '-set.releaseDate'
                },
                headers=headers,
                timeout=timeout_seconds
            )
            response.raise_for_status()
            data = response.json()
            cards = data.get('data', []) or []


        if len(cards) < 5:


            prefix_query = f'name:{search_for_api}*'
            response = session.get(
                'https://api.pokemontcg.io/v2/cards',
                params={
                    'q': prefix_query,
                    'pageSize': 20,
                    'select': 'id,name,set,images',
                    'orderBy': '-set.releaseDate'
                },
                headers=headers,
                timeout=timeout_seconds
            )
            response.raise_for_status()
            data = response.json()
            additional_cards = data.get('data', []) or []


            existing_ids = {c.get('id') for c in cards}
            for card in additional_cards:
                if card.get('id') not in existing_ids:
                    cards.append(card)
                    existing_ids.add(card.get('id'))


        cards = _filter_cards_by_name(cards, search_for_api)


        cards = _deduplicate_cards(cards)


        cards = cards[:15]


        save_to_cache(normalized_query, cards)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:

            api_failed = True
        elif e.response.status_code == 400:

            cards = []
        else:
            api_failed = True

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException):
        api_failed = True

    except Exception:
        api_failed = True


    if api_failed and len(cards) == 0:

        cached_fallback = load_from_cache(normalized_query)
        if cached_fallback is not None and len(cached_fallback) > 0:
            cards = cached_fallback
            from_cache = True
            error = None
        else:

            db_cards = (
                Card.query
                .filter(Card.name.ilike(f'{search_for_api}%'))
                .order_by(Card.name)
                .limit(20)
                .all()
            )
            if db_cards:
                cards = [
                    {
                        'id': c.api_card_id,
                        'name': c.name,
                        'images': {
                            'small': c.image_url_small,
                            'large': c.image_url_large or c.image_url_small,
                        },
                        'set': {'name': c.set_name or 'Unknown Set'},
                    }
                    for c in db_cards
                ]

                cards = _deduplicate_cards(cards)[:15]
                from_cache = True
                error = None
            else:
                error = "API_TIMEOUT"
                cards = []

    return cards, error, from_cache, api_failed

@bp.route('/search/cards')
@login_required
def search_cards():

    query = request.args.get('q', '').strip()
    cache_only = request.args.get('cache_only', 'false').lower() == 'true'
    cards = []
    error = None
    from_cache = False


    db.session.refresh(current_user)
    time_until_update = get_time_until_next_price_update()


    if len(query) < 2:
        if query:
            flash('Please enter at least 2 characters to search.', 'info')
        return render_template('search_cards.html',
                             title='Search Cards',
                             cards=[],
                             query=query,
                             error=None,
                             balance=current_user.balance,
                             time_until_update=time_until_update)

    if query:

        normalized_query = query.strip().lower()
        cached_cards = load_from_cache(normalized_query)

        if cache_only:

            if cached_cards is not None:
                cards = cached_cards
                from_cache = True
                flash('Showing cached results only (API may be slow).', 'info')
            else:
                flash('No cached results found. Try a regular search or wait for API.', 'info')
        else:

            cards, error, from_cache, api_failed = _perform_card_search(query)


            if (not cards or len(cards) == 0) and cached_cards is not None and len(cached_cards) > 0:
                cards = cached_cards
                from_cache = True
                error = None
                flash('Showing cached results.', 'info')
            elif api_failed and (not cards or len(cards) == 0):

                flash('The Pokemon TCG API is currently unresponsive. Please try again later or use cache-only mode.', 'warning')


        cards_with_prices = []
        if cards:
            for api_card in cards:

                if isinstance(api_card, dict):
                    card_data = api_card.copy()
                else:

                    card_data = {
                        'id': getattr(api_card, 'id', None),
                        'name': getattr(api_card, 'name', ''),
                        'images': getattr(api_card, 'images', {}),
                        'set': getattr(api_card, 'set', {})
                    }

                api_card_id = card_data.get('id')
                if not api_card_id:
                    continue


                db_card = Card.query.filter_by(api_card_id=api_card_id).first()
                if db_card:
                    card_price = initialize_card_price(db_card)
                    card_data['price'] = card_price
                else:

                    card_name = card_data.get('name', '')
                    set_name = card_data.get('set', {}).get('name', '')
                    estimated_price = _stable_price_seed(card_name, set_name)
                    card_data['price'] = estimated_price

                cards_with_prices.append(card_data)
        cards = cards_with_prices


    if cards:
        flash(f'Found {len(cards)} cards', 'success')
    elif query and not from_cache:

        flash('No cards found. Try a different search or use cache-only mode.', 'info')

    return render_template('search_cards.html',
                         title='Search Cards',
                         cards=cards,
                         query=query,
                         error=error,
                         balance=current_user.balance,
                         time_until_update=time_until_update)

@bp.route('/api/autocomplete')
@login_required
def autocomplete():

    query = request.args.get('q', '').strip().lower()

    if len(query) < 2:
        return jsonify({'suggestions': []})

    suggestions = []


    db_cards = Card.query.filter(Card.name.ilike(f'{query}%')).limit(10).all()
    for card in db_cards:
        if card.name not in suggestions:
            suggestions.append(card.name)


    for pokemon in COMMON_POKEMON:
        if pokemon.lower().startswith(query) and pokemon not in suggestions:
            suggestions.append(pokemon)
            if len(suggestions) >= 15:
                break


    suggestions.sort(key=lambda x: (not x.lower().startswith(query), x.lower()))

    return jsonify({'suggestions': suggestions[:15]})

@bp.route('/api/search/cards')
@login_required
def api_search_cards():

    query = request.args.get('q', '').strip()
    cache_only = request.args.get('cache_only', 'false').lower() == 'true'

    if len(query) < 2:
        return jsonify({
            'success': False,
            'error': 'Please enter at least 2 characters to search.',
            'cards': []
        })

    cards, error, from_cache, api_failed = _perform_card_search(query)


    cards_with_prices = []
    for api_card in cards:

        card_data = api_card.copy() if isinstance(api_card, dict) else dict(api_card)
        api_card_id = card_data.get('id')


        db_card = Card.query.filter_by(api_card_id=api_card_id).first()
        if db_card:
            card_price = initialize_card_price(db_card)
            card_data['price'] = card_price
        else:

            card_data['price'] = _stable_price_seed(
                card_data.get('name', ''),
                card_data.get('set', {}).get('name', '')
            )

        cards_with_prices.append(card_data)


    error_message = None
    if api_failed and len(cards_with_prices) == 0:
        error_message = "API_TIMEOUT"

    return jsonify({
        'success': error is None and len(cards_with_prices) > 0,
        'error': error_message or error,
        'cards': cards_with_prices,
        'from_cache': from_cache,
        'api_failed': api_failed,
        'count': len(cards_with_prices),
        'user_balance': current_user.balance
    })

@bp.route('/admin/clear-cache')
@login_required
def clear_cache():

    try:

        if CACHE_DIR.exists():
            for cache_file in CACHE_DIR.glob('*.json'):
                cache_file.unlink()
        flash('Cache cleared successfully! New searches will fetch fresh data from the API.', 'success')
    except Exception as e:
        flash(f'Error clearing cache: {str(e)}', 'danger')
    return redirect(url_for('main.search_cards'))

@bp.route('/admin/test-api')
@login_required
@admin_required
def test_api():


    _rate_limit_api_call()

    api_key = os.environ.get('POKEMON_TCG_API_KEY')
    headers = {'X-Api-Key': api_key} if api_key else {}
    session = get_api_session()

    try:

        response = session.get(
            'https://api.pokemontcg.io/v2/cards',
            params={'q': 'name:Pikachu*', 'pageSize': 1},
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'status': 'success',
                'message': 'API is working!',
                'response_time': f'{response.elapsed.total_seconds():.2f}s',
                'cards_found': len(data.get('data', []))
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'API returned status {response.status_code}',
                'status_code': response.status_code
            }), 500
    except requests.exceptions.Timeout:
        return jsonify({
            'status': 'error',
            'message': 'API request timed out after 10 seconds'
        }), 504
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        }), 500

@bp.route('/admin/update-prices')
@login_required
@admin_required
def update_prices():

    updated = update_daily_prices()
    flash(f'Updated prices for {updated} cards!', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/admin/bulk-import-cards', methods=['GET', 'POST'])
@login_required
@admin_required
def bulk_import_cards_endpoint():

    from app.models import Card

    if request.method == 'GET':

        total_cards = Card.query.count()
        pokemon_with_cards = db.session.query(Card.name).distinct().count()
        return jsonify({
            'status': 'ready',
            'total_cards': total_cards,
            'unique_pokemon': pokemon_with_cards,
            'message': f'Currently have {total_cards} cards from {pokemon_with_cards} Pokemon. POST to import more.'
        })


    data = request.get_json() or {}
    pokemon_list = data.get('pokemon_list', COMMON_POKEMON[:10])
    max_cards_per_pokemon = data.get('max_cards', 10)

    api_key = os.environ.get('POKEMON_TCG_API_KEY')
    headers = {'X-Api-Key': api_key} if api_key else {}
    headers['Accept-Encoding'] = 'gzip, deflate'
    session = get_api_session()
    session.headers.update(headers)

    results = {
        'imported': 0,
        'skipped': 0,
        'failed': 0,
        'pokemon_processed': []
    }

    for pokemon_name in pokemon_list:
        pokemon_result = {'name': pokemon_name, 'status': 'failed', 'imported': 0, 'skipped': 0}

        for attempt in range(3):
            try:

                response = session.get(
                    'https://api.pokemontcg.io/v2/cards',
                    params={
                        'q': f'name:"{pokemon_name}"',
                        'pageSize': max_cards_per_pokemon,
                        'select': 'id,name,set,images'
                    },
                    timeout=60
                )

                if response.status_code == 404:

                    response = session.get(
                        'https://api.pokemontcg.io/v2/cards',
                        params={
                            'q': f'name:{pokemon_name}*',
                            'pageSize': max_cards_per_pokemon,
                            'select': 'id,name,set,images'
                        },
                        timeout=60
                    )

                if response.status_code == 504:

                    if attempt < 2:
                        time.sleep(15 * (attempt + 1))
                        continue
                    else:
                        pokemon_result['status'] = 'gateway_timeout'
                        break

                response.raise_for_status()
                card_data_list = response.json().get('data', [])

                imported = 0
                skipped = 0

                for card_data in card_data_list:
                    api_card_id = card_data.get('id')
                    if not api_card_id:
                        continue

                    existing = Card.query.filter_by(api_card_id=api_card_id).first()
                    if existing:
                        skipped += 1
                        continue

                    card = Card(
                        api_card_id=api_card_id,
                        name=card_data.get('name', ''),
                        set_name=card_data.get('set', {}).get('name', ''),
                        image_url_small=card_data.get('images', {}).get('small', ''),
                        image_url_large=card_data.get('images', {}).get('large', ''),
                        price=100,
                        last_price_update=None
                    )
                    db.session.add(card)
                    imported += 1

                db.session.commit()
                pokemon_result['status'] = 'success'
                pokemon_result['imported'] = imported
                pokemon_result['skipped'] = skipped
                results['imported'] += imported
                results['skipped'] += skipped
                break

            except requests.exceptions.Timeout:
                if attempt < 2:
                    time.sleep(10 * (attempt + 1))
                    continue
                pokemon_result['status'] = 'timeout'
                results['failed'] += 1
                break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 504:
                    if attempt < 2:
                        time.sleep(15 * (attempt + 1))
                        continue
                    pokemon_result['status'] = 'gateway_timeout'
                    results['failed'] += 1
                    break
                elif e.response.status_code == 404:
                    pokemon_result['status'] = 'not_found'
                    break
                else:
                    pokemon_result['status'] = f'http_error_{e.response.status_code}'
                    results['failed'] += 1
                    break
            except Exception as e:
                db.session.rollback()
                pokemon_result['status'] = f'error: {str(e)[:50]}'
                results['failed'] += 1
                break

        results['pokemon_processed'].append(pokemon_result)


        time.sleep(2)

    return jsonify({
        'status': 'complete',
        'results': results,
        'message': f'Imported {results["imported"]} cards, skipped {results["skipped"]}, failed {results["failed"]}'
    })

@bp.route('/admin/clear-all-users', methods=['GET', 'POST'])
@login_required
@admin_required
def clear_all_users():

    if request.method == 'GET':
        return render_template('admin_clear_users.html', title='Clear All Users')


    try:


        OfferedCard.query.delete()
        RequestedCard.query.delete()


        Trade.query.delete()


        CollectionItem.query.delete()


        User.query.delete()



        db.session.commit()
        flash('All users and their data have been deleted. You will be logged out.', 'info')
        logout_user()
        return redirect(url_for('main.index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting users: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))

@bp.route('/cards/purchase', methods=['POST'])
@login_required
def purchase_card():

    api_card_id = request.form.get('api_card_id')
    card_name = request.form.get('card_name')
    set_name = request.form.get('set_name')
    image_small = request.form.get('image_small')
    image_large = request.form.get('image_large')
    condition = request.form.get('condition', 'Near Mint')

    if not api_card_id or not card_name:
        flash('Invalid card data.', 'danger')
        return redirect(url_for('main.search_cards'))


    card = Card.query.filter_by(api_card_id=api_card_id).first()

    if not card:

        card = Card(
            api_card_id=api_card_id,
            name=card_name,
            set_name=set_name,
            image_url_small=image_small,
            image_url_large=image_large
        )
        db.session.add(card)
        db.session.flush()


    base_price = initialize_card_price(card)


    condition_multipliers = {
        'Near Mint': 1.0,
        'Lightly Played': 0.8,
        'Moderately Played': 0.64,
        'Heavily Played': 0.512,
        'Damaged': 0.4096
    }
    multiplier = condition_multipliers.get(condition, 1.0)
    card_price = max(1, int(base_price * multiplier))


    if current_user.balance < card_price:
        flash(f'Insufficient funds! You need {card_price} PokeDollars but only have {current_user.balance}.', 'danger')
        return redirect(url_for('main.search_cards'))


    existing_item = CollectionItem.query.filter_by(
        user_id=current_user.id,
        card_id=card.id
    ).first()

    if existing_item:
        flash(f'You already have {card_name} in your collection!', 'info')
        return redirect(url_for('main.search_cards'))


    current_user.balance -= card_price
    collection_item = CollectionItem(
        user_id=current_user.id,
        card_id=card.id,
        condition=condition,
        is_for_trade=True,
        purchase_price=card_price,
        current_price=card_price
    )
    db.session.add(collection_item)
    db.session.commit()

    flash(f'{card_name} purchased for {card_price} PokeDollars! Your balance: {current_user.balance} PD', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/cards/<int:item_id>/toggle-trade', methods=['POST'])
@login_required
def toggle_trade_status(item_id):

    item = CollectionItem.query.get_or_404(item_id)


    if item.user_id != current_user.id:
        flash('You do not have permission to modify this card.', 'danger')
        return redirect(url_for('main.dashboard'))

    flash('This action is no longer supported.', 'info')
    return redirect(url_for('main.dashboard'))

@bp.route('/cards/<int:item_id>/sell', methods=['POST'])
@login_required
def sell_card(item_id):

    item = CollectionItem.query.get_or_404(item_id)


    if item.user_id != current_user.id:
        flash('You do not have permission to sell this card.', 'danger')
        return redirect(url_for('main.dashboard'))

    card = item.card_info


    pending_offered = OfferedCard.query.join(Trade).filter(
        OfferedCard.collection_item_id == item.id,
        Trade.status == TradeStatus.PENDING
    ).first()
    pending_requested = RequestedCard.query.join(Trade).filter(
        RequestedCard.collection_item_id == item.id,
        Trade.status == TradeStatus.PENDING
    ).first()
    if pending_offered or pending_requested:
        flash('This card is already part of a pending trade. Cancel the trade before selling.', 'danger')
        return redirect(url_for('main.dashboard'))


    current_value = item.current_price or calculate_condition_price(item.card_info.price, item.condition)


    sell_price = max(1, current_value // 2)

    current_user.balance += sell_price
    card_name = card.name
    condition = item.condition or 'Near Mint'


    db.session.delete(item)
    db.session.commit()

    flash(f'Sold {card_name} ({condition}) for {sell_price} PokeDollars!', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/cards/<int:item_id>/remove', methods=['POST'])
@login_required
def remove_card(item_id):

    item = CollectionItem.query.get_or_404(item_id)


    if item.user_id != current_user.id:
        flash('You do not have permission to remove this card.', 'danger')
        return redirect(url_for('main.dashboard'))

    card_name = item.card_info.name
    db.session.delete(item)
    db.session.commit()

    flash(f'{card_name} removed from your collection.', 'info')
    return redirect(url_for('main.dashboard'))

@bp.route('/trades')
@login_required
def trades():

    sent_trades = (
        Trade.query
        .filter(
            Trade.proposer_id == current_user.id,
            Trade.status == TradeStatus.PENDING
        )
        .order_by(Trade.created_at.desc())
        .all()
    )

    received_trades = (
        Trade.query
        .filter(
            Trade.receiver_id == current_user.id,
            Trade.status == TradeStatus.PENDING
        )
        .order_by(Trade.created_at.desc())
        .all()
    )

    return render_template('trades.html',
                         title='My Trades',
                         sent_trades=sent_trades,
                         received_trades=received_trades)

@bp.route('/trades/propose/<username>', methods=['GET', 'POST'])
@login_required
def propose_trade(username):

    receiver = User.query.filter_by(username=username).first_or_404()

    if receiver.id == current_user.id:
        flash('You cannot trade with yourself!', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':

        offered_item_ids = request.form.getlist('offered_items')

        requested_item_ids = request.form.getlist('requested_items')
        message = request.form.get('message', '').strip()
        proposer_currency = int(request.form.get('proposer_currency', 0) or 0)

        if not offered_item_ids:
            flash('You must offer at least one card.', 'danger')
            return redirect(url_for('main.propose_trade', username=username))

        if not requested_item_ids:
            flash('You must request at least one card.', 'danger')
            return redirect(url_for('main.propose_trade', username=username))


        if proposer_currency < 0:
            flash('Currency amount cannot be negative.', 'danger')
            return redirect(url_for('main.propose_trade', username=username))

        if proposer_currency > current_user.balance:
            flash(f'Insufficient funds. You have {current_user.balance} PD but tried to offer {proposer_currency} PD.', 'danger')
            return redirect(url_for('main.propose_trade', username=username))


        offered_items = CollectionItem.query.filter(
            CollectionItem.id.in_(offered_item_ids),
            CollectionItem.user_id == current_user.id
        ).all()

        if len(offered_items) != len(offered_item_ids):
            flash('Invalid cards selected for offering.', 'danger')
            return redirect(url_for('main.propose_trade', username=username))


        requested_items = CollectionItem.query.filter(
            CollectionItem.id.in_(requested_item_ids),
            CollectionItem.user_id == receiver.id
        ).all()

        if len(requested_items) != len(requested_item_ids):
            flash('Invalid cards selected for requesting.', 'danger')
            return redirect(url_for('main.propose_trade', username=username))


        all_card_ids = [item.id for item in offered_items + requested_items]
        existing_offered = OfferedCard.query.join(Trade).filter(
            OfferedCard.collection_item_id.in_(all_card_ids),
            Trade.status == TradeStatus.PENDING
        ).first()
        existing_requested = RequestedCard.query.join(Trade).filter(
            RequestedCard.collection_item_id.in_(all_card_ids),
            Trade.status == TradeStatus.PENDING
        ).first()
        if existing_offered or existing_requested:
            flash('Some cards are already in a pending trade.', 'danger')
            return redirect(url_for('main.propose_trade', username=username))


        trade = Trade(
            proposer_id=current_user.id,
            receiver_id=receiver.id,
            message=message,
            proposer_currency=proposer_currency,
            status=TradeStatus.PENDING
        )
        db.session.add(trade)
        db.session.flush()


        if proposer_currency > 0:
            current_user.balance -= proposer_currency


        for item in offered_items:
            offered_card = OfferedCard(
                trade_id=trade.id,
                collection_item_id=item.id,
                offering_user_id=current_user.id
            )
            db.session.add(offered_card)


        for item in requested_items:
            requested_card = RequestedCard(
                trade_id=trade.id,
                collection_item_id=item.id,
                requesting_user_id=current_user.id
            )
            db.session.add(requested_card)

        db.session.commit()
        flash(f'Trade proposal sent to {receiver.username}!', 'success')
        return redirect(url_for('main.trades'))



    proposer_cards = CollectionItem.query.filter_by(
        user_id=current_user.id
    ).all()


    receiver_cards = CollectionItem.query.filter_by(
        user_id=receiver.id
    ).all()


    db.session.refresh(current_user)

    return render_template('propose_trade.html',
                         title=f'Propose Trade to {receiver.username}',
                         receiver=receiver,
                         proposer_cards=proposer_cards,
                         receiver_cards=receiver_cards,
                         balance=current_user.balance)

@bp.route('/trades/<int:trade_id>/accept', methods=['POST'])
@login_required
def accept_trade(trade_id):

    trade = Trade.query.get_or_404(trade_id)

    if trade.receiver_id != current_user.id:
        flash('Only the receiving user can accept this trade. Make sure you are logged into the correct account.', 'danger')
        return redirect(url_for('main.trades'))

    if trade.status != TradeStatus.PENDING:
        flash('This trade is no longer pending.', 'danger')
        return redirect(url_for('main.trades'))


    offered_items = [oc.collection_item for oc in trade.offered_cards]
    requested_items = [rc.collection_item for rc in trade.requested_cards]


    if any(item.user_id != trade.proposer_id for item in offered_items):
        flash('Security error: Offered cards ownership has changed.', 'danger')
        return redirect(url_for('main.trades'))
    if any(item.user_id != trade.receiver_id for item in requested_items):
        flash('Security error: Requested cards ownership has changed.', 'danger')
        return redirect(url_for('main.trades'))


    for item in offered_items + requested_items:

        other_offered = OfferedCard.query.join(Trade).filter(
            OfferedCard.collection_item_id == item.id,
            Trade.status == TradeStatus.PENDING,
            Trade.id != trade.id
        ).first()

        other_requested = RequestedCard.query.join(Trade).filter(
            RequestedCard.collection_item_id == item.id,
            Trade.status == TradeStatus.PENDING,
            Trade.id != trade.id
        ).first()
        if other_offered or other_requested:
            flash('Some cards are already in another pending trade.', 'danger')
            return redirect(url_for('main.trades'))



    for item in offered_items:
        item.user_id = trade.receiver_id


    for item in requested_items:
        item.user_id = trade.proposer_id


    if trade.proposer_currency > 0:
        receiver_user = User.query.get(trade.receiver_id)
        receiver_user.balance += trade.proposer_currency



    trade.status = TradeStatus.ACCEPTED
    db.session.commit()

    currency_msg = f" and {trade.proposer_currency} PokeDollars" if trade.proposer_currency > 0 else ""
    flash(f'Trade accepted! Cards{currency_msg} have been transferred.', 'success')
    return redirect(url_for('main.trades'))

@bp.route('/trades/<int:trade_id>/reject', methods=['POST'])
@login_required
def reject_trade(trade_id):

    trade = Trade.query.get_or_404(trade_id)


    if current_user.id not in (trade.receiver_id, trade.proposer_id):
        flash('You do not have permission to modify this trade.', 'danger')
        return redirect(url_for('main.trades'))

    if trade.status != TradeStatus.PENDING:
        flash('This trade is no longer pending.', 'danger')
        return redirect(url_for('main.trades'))


    if trade.proposer_currency > 0:
        proposer_user = User.query.get(trade.proposer_id)
        proposer_user.balance += trade.proposer_currency


    if current_user.id == trade.receiver_id:
        trade.status = TradeStatus.REJECTED
    else:

        trade.status = TradeStatus.CANCELLED

    db.session.commit()

    if trade.status == TradeStatus.REJECTED:
        flash('Trade rejected. Currency has been returned if any was included.', 'info')
    else:
        flash('Trade cancelled. Any reserved currency has been returned.', 'info')
    return redirect(url_for('main.trades'))

@bp.route('/trades/<int:trade_id>/counter', methods=['GET', 'POST'])
@login_required
def counter_trade(trade_id):

    original_trade = Trade.query.get_or_404(trade_id)

    if original_trade.receiver_id != current_user.id:
        flash('You do not have permission to counter this trade.', 'danger')
        return redirect(url_for('main.trades'))

    if original_trade.status != TradeStatus.PENDING:
        flash('This trade is no longer pending.', 'danger')
        return redirect(url_for('main.trades'))

    if request.method == 'POST':

        offered_item_ids = request.form.getlist('offered_items')
        requested_item_ids = request.form.getlist('requested_items')
        message = request.form.get('message', '').strip()
        proposer_currency = int(request.form.get('proposer_currency', 0) or 0)

        if not offered_item_ids or not requested_item_ids:
            flash('You must offer and request at least one card.', 'danger')
            return redirect(url_for('main.counter_trade', trade_id=trade_id))


        if proposer_currency < 0:
            flash('Currency amount cannot be negative.', 'danger')
            return redirect(url_for('main.counter_trade', trade_id=trade_id))

        if proposer_currency > current_user.balance:
            flash(f'Insufficient funds. You have {current_user.balance} PD but tried to offer {proposer_currency} PD.', 'danger')
            return redirect(url_for('main.counter_trade', trade_id=trade_id))


        if original_trade.proposer_currency > 0:
            original_proposer = User.query.get(original_trade.proposer_id)
            original_proposer.balance += original_trade.proposer_currency


        original_trade.status = TradeStatus.CANCELLED


        counter_trade = Trade(
            proposer_id=current_user.id,
            receiver_id=original_trade.proposer_id,
            message=message,
            proposer_currency=proposer_currency,
            status=TradeStatus.PENDING
        )
        db.session.add(counter_trade)
        db.session.flush()


        if proposer_currency > 0:
            current_user.balance -= proposer_currency


        offered_items = CollectionItem.query.filter(
            CollectionItem.id.in_(offered_item_ids),
            CollectionItem.user_id == current_user.id
        ).all()

        for item in offered_items:
            offered_card = OfferedCard(
                trade_id=counter_trade.id,
                collection_item_id=item.id,
                offering_user_id=current_user.id
            )
            db.session.add(offered_card)


        requested_items = CollectionItem.query.filter(
            CollectionItem.id.in_(requested_item_ids),
            CollectionItem.user_id == original_trade.proposer_id
        ).all()

        for item in requested_items:
            requested_card = RequestedCard(
                trade_id=counter_trade.id,
                collection_item_id=item.id,
                requesting_user_id=current_user.id
            )
            db.session.add(requested_card)

        db.session.commit()
        flash('Counter-offer sent!', 'success')
        return redirect(url_for('main.trades'))


    proposer_cards = CollectionItem.query.filter_by(
        user_id=current_user.id
    ).all()

    original_proposer_cards = CollectionItem.query.filter_by(
        user_id=original_trade.proposer_id
    ).all()

    return render_template('counter_trade.html',
                         title='Counter Offer',
                         original_trade=original_trade,
                         proposer_cards=proposer_cards,
                         original_proposer_cards=original_proposer_cards)

@bp.route('/trades/<int:trade_id>')
@login_required
def view_trade(trade_id):

    trade = Trade.query.get_or_404(trade_id)


    if trade.proposer_id != current_user.id and trade.receiver_id != current_user.id:
        flash('You do not have permission to view this trade.', 'danger')
        return redirect(url_for('main.trades'))

    return render_template('trade_details.html',
                         title=f'Trade #{trade.id}',
                         trade=trade)