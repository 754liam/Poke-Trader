# Poke-Trader

A Pokémon card collecting and trading app built with Flask and PostgreSQL. Search cards, buy and sell with virtual coins, and trade with other users through offers and counteroffers.

Card data comes from the Pokémon TCG API. Hosted on Vercel.

[Live demo](https://pokemon-trader.vercel.app/)

## Run locally

```bash
git clone https://github.com/754liam/Poke-Trader
cd Poke-Trader
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your settings:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
POKEMON_TCG_API_KEY=your-api-key
ADMIN_USERS=your-email
```

Apply migrations and start the app:

```bash
flask --app api.index db upgrade
flask --app api.index run --debug
```

Open http://127.0.0.1:5000.
