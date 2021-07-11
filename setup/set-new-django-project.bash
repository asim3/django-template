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
	
	mv ./setup/requirements.txt ./requirements.txt
}


update-project-name() {
	sed -i -e "s/my_project_name/${name}/g" ./Makefile
	sed -i -e "s/my_project_name/${name}/g" ./README.md 
}


setup-django-settings() {
	mkdir ./${name}/${name}/settings/
	mv ./${name}/${name}/settings.py ./${name}/${name}/settings/base.py
	mv ./setup/settings/* ./${name}/${name}/settings/
}


setup-django-static() {
	mkdir -p ./${name}/static_resources/
	mv ./setup/static_resources/* ./${name}/static_resources/
}


copy-django-apps() {
	mv ./setup/apps/urls.py ./${name}/${name}/urls.py
	mv ./setup/apps/* ./${name}/
}


setup-heroku() {
	echo "web: gunicorn --chdir ${name} ${name}.wsgi" > ./Procfile
	echo "python-3.9.6" > ./runtime.txt
}


start-django-project
update-project-name
setup-django-settings
setup-django-static
copy-django-apps
setup-heroku
