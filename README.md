# django-template
Django Template


## Add New Django Project
```bash
make init
```


## Install requirements.txt & Migrate
```bash
make install
```


## Run Server
```bash
make
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


## Config Vars (env)
- `AWS_ACCESS_KEY_ID` = `********`
- `AWS_SECRET_ACCESS_KEY` = `********`
- `DATABASE_URL` = `postgres://***:*****@pg.com:5432/***`
- `DJANGO_ALLOWED_HOSTS` = `my_project_name.com,my_project_name.sa`
- `DJANGO_SECRET_KEY` = `********`
- `DJANGO_SETTINGS_MODULE` = `my_project_name.settings.staging`
- `DJANGO_SETTINGS_MODULE` = `my_project_name.settings.production`



## Run Shell
```bash
make shell
```


## AWS
### CORS: Cross-origin resource sharing
```json
[
    {
        "AllowedHeaders": [],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "https://www.example1.com",
            "https://www.example2.com",
            "https://project-staging.herokuapp.com"
        ],
        "ExposeHeaders": []
    }
]
```


# anti spam
[reCaptcha](https://www.google.com/recaptcha/admin)


## env
- `RECAPTCHA_SITEKEY`
- `RECAPTCHA_SECRETKEY`