run:
	fastapi dev ./app/main.py

createmigration:
	alembic revision --autogenerate -m "First migration"

runmigration:
	alembic upgrade head

lint:
	poetry run pre-commit run --all-files

docker-build:
	docker build -t my_study_api .

docker-run:
	docker run -d -p 9000:9000 --name my_study_api my_study_api

docker-logs:
	docker logs -f my-study-api-container
