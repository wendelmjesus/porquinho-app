# Porquinho

**Porquinho** is a personal finance desktop app built with Python, PySide6, Qt/QSS, and SQLite.

The app helps track income, expenses, categories, goals, reports, and financial progress in a simple desktop interface.

## Features

- Financial dashboard with balance, income, and expense summaries.
- Recent transactions panel with quick edit actions.
- Balance evolution chart based on saved transactions.
- Income and expense transaction management.
- Transaction search, filtering, editing, and removal.
- Custom categories for income and expenses.
- Financial goals with target amount, saved amount, and progress percentage.
- Goal deposits after a goal has already been created.
- Reports by category.
- Export reports to CSV, compatible with Excel.
- Light and dark mode.
- Local SQLite persistence.

## Tech Stack

- Python
- PySide6
- Qt / QSS
- SQLite

## Project Structure

```text
finance-app/
  app/
    assets/
      porquinho_logo.png

    database/
      __init__.py
      manager.py
      schema.sql

    widgets/
      __init__.py
      finance_chart.py

    __init__.py
    main_window.py
    styles.py

  data/
    .gitkeep
    porquinho.db

  main.py
  requirements.txt
  README.md
```

## Local Data

Porquinho stores local app data in:

```text
data/porquinho.db
```

This file contains personal financial data and is intentionally ignored by Git.

The database structure is versioned separately in:

```text
app/database/schema.sql
```

## Running The App

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 main.py
```

## GitHub Notes

The repository is configured to avoid committing local/private files such as:

- SQLite database files in `data/`
- exported CSV reports
- Python cache files
- virtual environment files

Only `data/.gitkeep` is committed so the `data/` folder exists in fresh clones.

## Status

Work in progress. The app is functional, but the UI, data model, reports, and persistence layer may continue to evolve.

## License

This project is licensed under the MIT License.
