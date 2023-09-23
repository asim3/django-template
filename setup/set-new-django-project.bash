#!/bin/bash

set -eu

# Fail on a single failed command in a pipeline
set -o pipefail 


echo -n "Project Name: "
read name


start-django-project() {
	if [ ! -d ~/.venv/${name} ]; then python3 -m venv ~/.venv/${name}; fi;

	source ~/.venv/${name}/bin/activate
	
	mv ./setup/requirements.txt ./requirements.txt
	
	pip3 install -r ./requirements.txt

	django-admin startproject ${name}
}


update-project-name() {
	sed -i -e "s/my_project_name/${name}/g" ./Makefile
	sed -i -e "s/my_project_name/${name}/g" ./README.md
	sed -i -e "s/my_project_name/${name}/g" ./setup/Dockerfile
	sed -i -e "s/my_project_name/${name}/g" ./setup/docker-compose.yml
	sed -i -e "s/my_project_name/${name}/g" ./.github/workflows/docker-test.yml
	sed -i -e "s/my_project_name/${name}/g" ./.github/workflows/docker-ci.yml
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


setup-dotenv() {
	cp ./setup/.env.sample ./${name}/.env
	mv ./setup/.env.sample ./${name}/.env.sample
}


setup-docker() {
	mv ./setup/Dockerfile          ./
	mv ./setup/docker-compose.yml  ./
}


copy-django-apps() {
	mv ./setup/apps/urls.py ./${name}/${name}/urls.py
	mv ./setup/apps/* ./${name}/
}



remove-setup-files() {
	rm -rf ./setup/
}


start-django-project
update-project-name
setup-django-settings
setup-django-static
setup-dotenv
setup-docker
copy-django-apps
remove-setup-files
