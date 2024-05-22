run:
	fastapi dev ./app/main.py

createmigration:
	alembic revision -m "First migration"

runmigration:
	alembic upgrade head