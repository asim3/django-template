# django-template
Django Template


## Config Vars (env)
- `DJANGO_SETTINGS_MODULE` = `my_project_name.settings.staging`
- `DJANGO_SETTINGS_MODULE` = `my_project_name.settings.production`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`


## Add New Django Project
```bash
make init
```


## Run Server
```bash
make
```


## Install requirements.txt & Migrate
```bash
make install
```


## Add Super User
```bash
make user
```


## Add New Django App
```bash
make new app=my_app
```


## Run Tests
```bash
make test
```


## Run Shell
```bash
make shell
```
