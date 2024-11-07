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

### Step 4: To Start Redis Server on Ubuntu-WSL

```bash
sudo start redis-server
```

### Step 5: To Check Redis Server is running

```bash
redis-cli ping
```

### Step 6: To Start Celery Worker

```bash
celery -A task worker --loglevel=info -P eventlet
```

### Step 5: To Start Celery beat

```bash
celery -A task beat --loglevel=info
```
