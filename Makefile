test:
	black --check .
	flake8 .
	mypy --strict
	pytest --cov=videoprof --cov-fail-under=75 --cov-report term-missing tests/*
