# Sneakers

Attention! This repository was created for educational purposes. I'm not responsible for anything. Don't try to use it!

API with sneakers

stack:
- flask
- postgresql

## TODO

- [x] tests
- [x] database loading
- [ ] errors
- [ ] /v1/brands
- [ ] paging
- [ ] limit & offset
- [ ] sort
- [ ] CRUD?
- [ ] manage.py useless?
- [ ] Limiting which fields are returned by the API
- [ ] containers
- [ ] ci/cd pipeline
- [ ] bulk insert to db session.bulk_save_objects([cookiemon, cakeeater, pieperson])
- [ ] generate any count of sneakers by fake factory in tests
- [ ] tests coverage > 90%
- [ ] X-Total-Count, Link, Content-Range headers, has_more field?
- [ ] How to test 500 error?

## Endpoints

- /v1/sneakers
- /v1/sneakers/{sneaker_id}

## Responses

Almost every API response contains two top-level fields: items and errors. Each of them is an array, which can contain 0 or more items.

## First run

Install dependecies:

```Bash
pipenv install
```

Create PostgreSQL database:

```Bash
CREATE DATABASE sneakers
```

Set up database:

```Bash
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/sneakers"
pipenv run flask db init
pipenv run flask db migrate
pipenv run flask db upgrade
```

Create `.env` file:

```Ini
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/sneakers"
export FLASK_ENV=development
```

Run Flask app:

```Bash
pipenv run flask run
```

Warm-up to create a table/schema:

```Bash
curl 'http://127.0.0.1:5000/v1/sneakers'
```

Run db_loader.py to populate database:

```Bash
pipenv run python db_loader.py
```

## Testing

Create `.env.test` file:

```Ini
export APP_SETTINGS="config.TestingConfig"
export DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/sneakers-test"
export FLASK_ENV=test
```

Change env config and run tests witch command:

```Bash
PIPENV_DOTENV_LOCATION=.env.test pipenv run pytest
```

## Data load

Script `db_loader.py` populates database from this dataset automatically. To manually look at the data:

```Bash
curl -so thesneakerdatabase-nike.json 'https://www.thesneakerdatabase.com/api/getData?brand=Nike' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36' \
  -H 'Accept: */*' \
  -H 'Origin: https://thesneakerdatabase.com' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://thesneakerdatabase.com/' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7' \
  --compressed


cat thesneakerdatabase-nike.json| jq -r '.data[0]'
cat thesneakerdatabase-nike.json| jq -r '.data | length'
```
