# Poke-Trader

A Pokémon TCG collecting and trading app built with Flask.

Users can search real cards from the Pokémon TCG API, buy and sell them with virtual currency, build a collection, and trade cards with other users.

**[Live Demo](https://pokemon-trader.vercel.app/)**

## Features

- Search cards using the Pokémon TCG API
- Buy and sell cards with virtual coins
- Track card condition and value
- Build and manage a personal collection
- Trade cards and coins with other users
- Accept, reject, or counter trade offers
- Browse other users' collections
- Admin tools for managing cards, prices, and users

## Tech Stack

- Flask
- PostgreSQL / SQLAlchemy
- Jinja2
- Flask-Login
- Flask-Migrate
- Pokémon TCG API
- Vercel

## Project Structure

```text id="hr2p33"
Poke-Trader/
├── api/
│   └── index.py
├── app/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── models.py
│   └── __init__.py
├── migrations/
├── config.py
├── requirements.txt
└── vercel.json
```

## Running Locally

```bash id="5g4nvu"
git clone https://github.com/754liam/Poke-Trader
cd Poke-Trader

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env id="5idq1r"
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
POKEMON_TCG_API_KEY=your-api-key
ADMIN_USERS=your-email
```

Run the database migrations:

```bash id="652b83"
flask --app api.index db upgrade
```

Start the app:

```bash id="sok177"
flask --app api.index run --debug
```

Then open `http://127.0.0.1:5000`.

## Deployment

The app is deployed on Vercel with PostgreSQL as the database.
