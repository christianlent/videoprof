test:
	uv run ruff format --check .
	uv run ruff check .
	uv run mypy --strict
	uv run pytest --cov=videoprof --cov-fail-under=75 --cov-report term-missing tests/*

format:
	uv run ruff format .
	uv run ruff check --fix .
