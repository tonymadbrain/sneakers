.PHONY: test

test:
	PIPENV_DOTENV_LOCATION=.env.test pipenv run pytest

dev:
	pipenv run flask run
