# Poke-Trader

A Pokémon TCG collecting and trading web app built with Flask. Search real cards from the [Pokémon TCG API](https://pokemontcg.io/), buy them with virtual currency, build a collection, and trade with other users — including counter-offers and coin sweeteners.

**[Live demo →](https://pokemon-trader.vercel.app/)**

## Features

- **Card search** — live search against the Pokémon TCG API with autocomplete, a 24-hour file cache, and pre-cached data for popular Pokémon so common searches are instant.
- **Virtual economy** — every new user starts with 1,000 coins. Card prices are seeded deterministically per card and re-rolled daily, and a card's value is adjusted by its condition (Near Mint, Played, etc.).
- **Collections** — buy and sell cards, track purchase price vs. current value, and mark individual cards as available (or not) for trade.
- **Trading** — propose trades to other users offering any mix of your cards plus coins, and request cards from their collection. Recipients can accept, reject, or send a counter-offer. Cards locked in a pending trade can't be traded twice, and coins are escrowed when an offer is sent and refunded if it falls through.
- **User profiles** — search for other users and browse their public collections.
- **Admin tools** — bulk-import cards for common Pokémon, refresh prices, clear the API cache, and manage users. Admin access is granted via the `ADMIN_USERS` environment variable.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Flask (app factory + blueprints) |
| Database | PostgreSQL via Flask-SQLAlchemy, migrations via Flask-Migrate (Alembic) |
| Auth | Flask-Login sessions, Flask-Bcrypt password hashing, Flask-WTF CSRF protection |
| Frontend | Server-rendered Jinja2 templates |
| Card data | Pokémon TCG API v2 with local file caching |
| Deployment | Vercel serverless (`api/index.py`), Gunicorn-compatible |

## Project structure

```
Poke-Trader/
├── api/index.py           # Vercel serverless entry point
├── config.py              # Environment-based configuration
├── app/
│   ├── __init__.py        # App factory and extension setup
│   ├── auth.py            # Register / login / logout
│   ├── models.py          # User, Card, CollectionItem, Trade models
│   ├── decorators.py      # Admin permission helpers
│   ├── precached_pokemon.py  # Bundled card data for instant search
│   ├── routes/
│   │   ├── pages.py       # Home, dashboard, profiles, user search
│   │   ├── cards.py       # Card search, purchase, sell, trade toggles
│   │   ├── trades.py      # Propose, accept, reject, counter trades
│   │   └── admin.py       # Cache, pricing, and import tools
│   ├── services/
│   │   ├── pokemon_api.py # TCG API client + caching
│   │   ├── pricing.py     # Daily pricing and condition multipliers
│   │   ├── trades.py      # Trade creation and validation
│   │   └── bulk_import.py # Bulk card import
│   └── templates/         # Jinja2 templates
├── migrations/            # Alembic database migrations
└── vercel.json            # Vercel routing and build config
```

## Getting started

### Prerequisites

- Python 3.11+
- A PostgreSQL database (or any SQLAlchemy-compatible database URL)
- A free [Pokémon TCG API key](https://dev.pokemontcg.io/) (optional but recommended — raises rate limits)

### Setup

1. **Clone and install dependencies**

```bash
git clone <repo-url> Poke-Trader
cd Poke-Trader
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Configure the environment** — create a `.env` file in the project root:

```bash
SECRET_KEY=change-me-to-something-random
DATABASE_URL=postgresql://user:password@localhost:5432/poketrader
POKEMON_TCG_API_KEY=your-api-key        # optional
ADMIN_USERS=you@example.com             # comma-separated emails/usernames
```

3. **Initialize the database**

```bash
flask --app api.index db upgrade
```

4. **Run the app**

```bash
flask --app api.index run --debug
```

Then open http://127.0.0.1:5000, register an account, and start collecting.

## Deployment

The project is set up for Vercel: `vercel.json` routes all traffic to the serverless entry point in `api/index.py` and serves static assets directly. Set the same environment variables (`SECRET_KEY`, `DATABASE_URL`, `POKEMON_TCG_API_KEY`, `ADMIN_USERS`) in your Vercel project settings. Heroku-style `postgres://` database URLs are normalized automatically.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes (production) | Flask session signing key; an insecure dev default is used if unset |
| `DATABASE_URL` | Yes | SQLAlchemy database URL; `postgres://` is rewritten to `postgresql://` |
| `POKEMON_TCG_API_KEY` | No | Pokémon TCG API key for higher rate limits |
| `ADMIN_USERS` | No | Comma-separated emails or usernames granted admin access |
| `POKETRADER_CACHE_DIR` | No | Override for the API cache directory (defaults to `cache/`, or `/tmp` on Vercel) |
