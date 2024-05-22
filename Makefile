SHELL=/bin/bash

PROJECT_NAME=my_project_name

DOCKER_RUN=docker compose run app


main: run

init:
	@sed -i -e 's/\r$$//' ./setup/set-new-django-project.bash
	@./setup/set-new-django-project.bash


# make test args=my_app
tests: check
	${DOCKER_RUN} "python3 manage.py test ${args};"


# make new app=my_app
new:
	${DOCKER_RUN} "python3 manage.py startapp ${app};"


user:
	${DOCKER_RUN} "python3 manage.py createsuperuser;"


tra:
	${DOCKER_RUN} "if [ ! -d ./locale ]; then mkdir locale; fi;"
	${DOCKER_RUN} "python3 manage.py makemessages -l ar"
	${DOCKER_RUN} "python3 manage.py compilemessages"


run:
	docker compose up --build --remove-orphans


make_migrations:
	${DOCKER_RUN} "python3 manage.py makemigrations --dry-run"
	${DOCKER_RUN} "python3 manage.py makemigrations"
	- ${DOCKER_RUN} "python3 manage.py generateschema --file ./templates/api/openapi-schema.yaml"


shell:
	${DOCKER_RUN} "python3 manage.py shell"


# make data-migrations app=my_app
data-migrations:
	${DOCKER_RUN} "python3 manage.py makemigrations --empty ${app}"


check:
	${DOCKER_RUN} "python3 manage.py check --deploy \
	--settings ${PROJECT_NAME}.settings.production \
	--fail-level WARNING \
	&& echo 'production settings looks good'"
	${DOCKER_RUN} "mkdir -p ./media/backup"
	- ${DOCKER_RUN} "cp ./db.sqlite3 ./media/backup/db_$$(date +'%Y-%m-%d_%H-%M-%S').sqlite3"
