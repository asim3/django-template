SHELL=/bin/bash

ACTIVATE=source ~/.venv/${PROJECT_NAME}/bin/activate &&

PROJECT_NAME=my_project_name

CD=${ACTIVATE} cd ./${PROJECT_NAME} &&


main: run

init:
	@sed -i -e 's/\r$$//' ./setup/set-new-django-project.bash
	@./setup/set-new-django-project.bash
	eval "make install"


venv:
	if [ ! -d ~/.venv/${PROJECT_NAME} ]; then python3 -m venv ~/.venv/${PROJECT_NAME}; fi;
	if [ ! -f ./${PROJECT_NAME}/.env ]; then cp ./${PROJECT_NAME}/.env.sample ./${PROJECT_NAME}/.env; fi;


install: venv sql-backup
	${ACTIVATE} pip3 install -r ./requirements.txt
	${CD} python3 manage.py makemigrations --dry-run
	${CD} python3 manage.py makemigrations
	${CD} python3 manage.py migrate
	- ${CD} python3 manage.py generateschema --file ./templates/api/openapi-schema.yaml
	- ${CD} python3 manage.py collectstatic --noinput


# make test args=my_app
tests: check
	if [ -d ~/.venv/${PROJECT_NAME} ]; then ${CD} python3 manage.py test ${args}; fi;


# make new app=my_app
new:
	${CD} python3 manage.py startapp ${app};


user:
	${CD} python3 manage.py createsuperuser;


tra:
	${CD} if [ ! -d ./locale ]; then mkdir locale; fi;
	${CD} python3 manage.py makemessages -l ar
	${CD} python3 manage.py compilemessages


run:
	${CD} python3 manage.py runserver


docker:
	sudo docker-compose config
	sudo docker-compose up --build --remove-orphans


shell:
	${CD} python3 manage.py shell


# make data-migrations app=my_app
data-migrations:
	${CD} python3 manage.py makemigrations --empty ${app}


check:
	${CD} python3 manage.py check --deploy \
	--settings ${PROJECT_NAME}.settings.production \
	--fail-level WARNING \
	&& echo 'production settings looks good'


production:
	- git fetch origin production
	git checkout production || git checkout -b production
	git merge main
	git push origin production 
	git checkout main


sql-backup:
	${CD} mkdir -p ./media/backup
	- ${CD} cp ./db.sqlite3 ./media/backup/db_$$(date +'%Y-%m-%d_%H-%M-%S').sqlite3

tag:
	git tag -a $$(git tag -l --sort=-creatordate 'v-*' | head -n 1 | awk -F. -v OFS=. '{$$NF += 1 ; print}') -m 'Added by $$(whoami) using Makefile v2'
	git push origin --tags
