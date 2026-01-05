# PokeTrader Platform

A full-stack trading platform built with **Flask** and **PostgreSQL**. This application features a secure authentication system, an automated market with deterministic pricing algorithms, and a complex many-to-many trading architecture.

## What it's all about

This project is centered around hosting a Pokemon card market where users can buy, sell, and trade. Each user starts off with 1000 PD (Poke Dollars) and is able to purchase cards of fluctuating prices (1-1000) which update every day. The Pokemon TCG API is used for extracting card data and a Neon provided PostgreSQL manager is used for managing inventory/trade systems.
## Local Setup

```bash
# Environment variables
Set up a .env file with proper API keys (look at config.py for context)
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/poketrader-platform.git](https://github.com/YOUR_USERNAME/poketrader-platform.git)

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
