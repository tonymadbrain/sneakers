# Sneakers

Attention! This repository was created for educational purposes. I'm not responsible. Don't try to use it!

API with sneakers

tech:
* flask
* postgresql

## Endpoints

* /v1/sneakers
* /v1/sneakers/nike
* /v1/sneakers/nike/{sneaker_id}

## TODO

* tests
* database loading
* /v1/brands
* paging
* limit
* sort
* POST with JSON?
* manage.py useless?

## Data load

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

## Database

```Bash
CREATE DATABASE sneakers
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/sneakers"
flask db init
flask db migrate
flask db upgrade
curl -X POST 'http://127.0.0.1:5000/v1/sneakers?name=Nike%20Free%20Run%20Trail%20Black%20Anthracite&brand=Nike&release_date=2021-08-01'
```
