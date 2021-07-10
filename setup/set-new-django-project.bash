#!/bin/bash

set -eu

# Fail on a single failed command in a pipeline
set -o pipefail 


echo -n "Project Name: "
read name


start-django-project() {
	python3 -m venv .venv
    source ./.venv/bin/activate

	pip3 install django
	django-admin startproject ${name}
	
    echo -e 'django\ndjango-heroku\ngunicorn' > ./requirements.txt
}


update-project-name-in-makefile() {
	sed -i -e "s/my_project_name/${name}/" ./Makefile
}


setup-django-settings() {
	mkdir ./${name}/${name}/settings/
	mv ./${name}/${name}/settings.py ./${name}/${name}/settings/base.py
	mv ./setup/settings/* ./${name}/${name}/settings/
}


setup-django-static() {
	mkdir -p ./${name}/static_resources/css
	touch    ./${name}/static_resources/css/main.css
	
	mkdir -p ./${name}/static_resources/js
	touch    ./${name}/static_resources/js/main.js
}


setup-heroku() {
	echo "web: gunicorn --chdir ${name} ${name}.wsgi" > ./Procfile
	echo "python-3.9.6" > ./runtime.txt
}


start-django-project
update-project-name-in-makefile
setup-django-settings
setup-django-static
setup-heroku
