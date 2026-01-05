# Script to bulk import Pokemon cards from TCG API into database
# Flask, Flask-SQLAlchemy, requests

from app import create_app, db
from app.models import Card
import requests
import os
import time
from datetime import date
app = create_app()
POKEMON_LIST = ['Pikachu', 'Charizard', 'Blastoise', 'Venusaur', 'Mewtwo', 'Mew', 'Lucario', 'Garchomp', 'Gengar', 'Snorlax', 'Dragonite', 'Tyranitar', 'Rayquaza', 'Groudon', 'Kyogre', 'Dialga', 'Palkia', 'Giratina', 'Arceus', 'Zekrom', 'Reshiram', 'Kyurem', 'Xerneas', 'Yveltal', 'Zygarde', 'Solgaleo', 'Lunala', 'Necrozma', 'Eternatus', 'Zacian', 'Zamazenta', 'Urshifu', 'Calyrex', 'Koraidon', 'Miraidon', 'Ogerpon', 'Bulbasaur', 'Charmander', 'Squirtle', 'Eevee', 'Jigglypuff', 'Meowth', 'Psyduck', 'Machop', 'Abra', 'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Vaporeon', 'Jolteon', 'Flareon', 'Aerodactyl', 'Snorlax']

def get_api_session():
    print(f'  Importing {pokemon_name}...', end=' ', flush=True)
    for attempt in range(max_retries):
        try:
            response = session.get('https://api.pokemontcg.io/v2/cards', params={'q': f'name:"{pokemon_name}"', 'pageSize': max_cards, 'select': 'id,name,set,images'}, timeout=60)
            if response.status_code != 200:
                response = session.get('https://api.pokemontcg.io/v2/cards', params={'q': f'name:{pokemon_name}*', 'pageSize': max_cards, 'select': 'id,name,set,images'}, timeout=60)
            if response.status_code == 504:
                raise requests.exceptions.HTTPError(f'504 Gateway Timeout', response=response)
            response.raise_for_status()
            data = response.json()
            cards = data.get('data', [])
            imported = 0
            skipped = 0
            for card_data in cards:
                api_card_id = card_data.get('id')
                if not api_card_id:
                    continue
                existing = Card.query.filter_by(api_card_id=api_card_id).first()
                if existing:
                    skipped += 1
                    continue
                card = Card(api_card_id=api_card_id, name=card_data.get('name', ''), set_name=card_data.get('set', {}).get('name', ''), image_url_small=card_data.get('images', {}).get('small', ''), image_url_large=card_data.get('images', {}).get('large', ''), price=100, last_price_update=None)
                db.session.add(card)
                imported += 1
            db.session.commit()
            print(f'✅ {imported} imported, {skipped} skipped')
            return imported
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f'⏳ Timeout (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s...', end=' ', flush=True)
                time.sleep(wait_time)
                continue
            else:
                db.session.rollback()
                print(f'❌ Timeout after {max_retries} attempts')
                return 0
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 504:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10
                    print(f'⏳ Gateway timeout (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s...', end=' ', flush=True)
                    time.sleep(wait_time)
                    continue
                else:
                    db.session.rollback()
                    print(f'❌ Gateway timeout after {max_retries} attempts')
                    return 0
            elif e.response.status_code == 404:
                db.session.rollback()
                print(f'⚠️  No cards found (404)')
                return 0
            elif attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f'⚠️  HTTP {e.response.status_code} (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s...', end=' ', flush=True)
                time.sleep(wait_time)
                continue
            else:
                db.session.rollback()
                print(f'❌ HTTP {e.response.status_code} after {max_retries} attempts')
                return 0
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f'🔌 Connection error (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s...', end=' ', flush=True)
                time.sleep(wait_time)
                continue
            else:
                db.session.rollback()
                print(f'❌ Connection failed after {max_retries} attempts')
                return 0
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            if len(error_msg) > 80:
                error_msg = error_msg[:77] + '...'
            print(f'❌ Error: {error_msg}')
            return 0
    return 0

def main():
    with app.app_context():
        print('🚀 Starting bulk card import...')
        print(f'📋 Will import up to 10 cards each for {len(POKEMON_LIST)} Pokemon')
        print('⏳ This may take a few minutes...\n')
        session = get_api_session()
        total_imported = 0
        for i, pokemon in enumerate(POKEMON_LIST, 1):
            print(f'[{i}/{len(POKEMON_LIST)}] ', end='')
            imported = import_pokemon_cards(pokemon, session)
            total_imported += imported
            if i < len(POKEMON_LIST):
                time.sleep(2.0)
        print(f'\n✅ Import complete!')
        print(f'📊 Total cards imported: {total_imported}')
        print(f'💡 Cards are now in your database and searches will be much faster!')
if __name__ == '__main__':
    main()