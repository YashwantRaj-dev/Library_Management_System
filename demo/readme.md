# Welcome to the documentation

### Step 1: Install the package

activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install poetry requirements

```bash
pip install poetry
```

```bash
poetry install
```

### Project structure

```
/demo
    /models
        user.py
    /templates
         index.html
         register.html
    app.py
    config.py
    pyproject.toml
```

### Step 2: Create the database

```bash
poetry run flask db init
poetry run flask db migrate -m "Initial migration"
poetry run flask db upgrade
```
### Step 3: Run the application

```bash
poetry run python app.py
```