#!/bin/bash

set -eu

# Fail on a single failed command in a pipeline
set -o pipefail 


name="${1}"


start-django-project() {
	python3 -m venv .venv
    source ./.venv/bin/activate

	pip3 install django
	django-admin startproject ${name}
	
    echo 'django' > ./${name}/requirements.txt
}


update-project-name-in-makefile() {
	sed -i -e "s/my_project_name/${name}/" ./Makefile
}


setup-django-settings() {
	SECRET_KEY="SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')"
	DEBUG="DEBUG = os.getenv('DJANGO_DEBUG', False) in (True, 'True')"
	ALLOWED_HOSTS="ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')"

	sed -i -e "s/^SECRET_KEY.*/${SECRET_KEY}/" ./${name}/${name}/settings.py
	sed -i -e "s/^DEBUG.*/${DEBUG}/" ./${name}/${name}/settings.py
	sed -i -e "s/^ALLOWED_HOSTS.*/${ALLOWED_HOSTS}/" ./${name}/${name}/settings.py 
	
	sed -i -e "s/import Path/import Path\nimport os/" ./${name}/${name}/settings.py
}


start-django-project
update-project-name-in-makefile
setup-django-settings
