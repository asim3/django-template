# django-template
Django Template


## Config Vars (env)
- `DJANGO_SETTINGS_MODULE` = `my_project_name.settings.test`
- `DJANGO_SETTINGS_MODULE` = `my_project_name.settings.production`

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`


## Add New Django Project
```bash
make init name=my_project_name
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
