SHELL=/bin/bash

ACTIVATE=source ./.venv/bin/activate &&

PROJECT_NAME=my_project_name

CD=${ACTIVATE} cd ./${PROJECT_NAME} &&


export DJANGO_SECRET_KEY="top-secret"
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS=*,127.0.0.1,localhost


main: run

init: 
	./setup/set-new-django-project.bash
	echo -e "#####################################\n#                                   #\n#    Please Run [ make install ]    #\n#                                   #\n#####################################"


venv:
	if [ ! -d ./.venv ]; then python3 -m venv ./.venv; fi;


install: venv sql-backup
	${ACTIVATE} pip3 install -r ./requirements.txt
	${CD} python3 manage.py makemigrations --dry-run
	${CD} python3 manage.py makemigrations
	${CD} python3 manage.py migrate
	- ${CD} python3 manage.py collectstatic --noinput


# make test args=my_app
tests:
	if [ -d ./.venv ]; then ${CD} python3 manage.py test ${args}; fi;


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
	${CD} export DJANGO_SETTINGS_MODULE=${PROJECT_NAME}.settings.production; python manage.py check --deploy


production:
	- git fetch origin production
	git checkout production || git checkout -b production
	git merge main
	git push origin production 
	git checkout main

backup:
	heroku pg:backups:capture -a ${PROJECT_NAME}-production
	heroku pg:backups:restore $$(heroku pg:backups:url -a ${PROJECT_NAME}-production) \
		--confirm=${PROJECT_NAME}-staging -a ${PROJECT_NAME}-staging

sql-backup:
	${CD} mkdir -p ./media/backup
	- ${CD} cp ./db.sqlite3 ./media/backup/db_$$(date +'%Y-%m-%d_%H-%M-%S').sqlite3
