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
	sed -i -e "s/my_project_name/${name}/g" ./setup/Dockerfile 
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


setup-kubernetes() {
	mv ./setup/Dockerfile ./
	mv ./setup/docker-compose.yaml ./
	mv ./setup/manifest ./
}


copy-django-apps() {
	mv ./setup/apps/urls.py ./${name}/${name}/urls.py
	mv ./setup/apps/* ./${name}/
}


setup-heroku() {
	echo "release: cd ${name} && python3 manage.py migrate" > ./Procfile
	echo "web: gunicorn --chdir ${name} --workers 3 ${name}.wsgi" >> ./Procfile
	echo "python-3.9.6" > ./runtime.txt
}


remove-setup-files() {
	rm -rf ./setup/
}


commit-and-push() {
	code .
	git add .
	git commit -m "setting up a new Django project"
	git push origin main 
}


start-django-project
update-project-name
setup-django-settings
setup-django-static
setup-kubernetes
copy-django-apps
setup-heroku
remove-setup-files

repository_name=$(basename $(pwd))
if [ ! "$repository_name" = "django-template" ]; then
	commit-and-push
fi
