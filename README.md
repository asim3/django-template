# django-template
Django Template


| Command               | Function                           |
| --------------------- | ---------------------------------- |
| `make init`           | Add New Django Project             |
| `make install`        | Install requirements.txt & Migrate |
| `make user`           | Add Super User                     |
| `make new app=my_app` | Add New Django App                 |
| `make`                | Run Server                         |
| `make test`           | Run Tests                          |
| `make shell`          | Run Shell                          |


---


## Config Vars (env)
- `DJANGO_SETTINGS_MODULE` = `my_project_name.settings.production`
- `DJANGO_ALLOWED_HOSTS` = `my_project_name.com,my_project_name.sa`
- `DJANGO_SECRET_KEY` = `********`
- `REST_SIGNING_KEY` = `********`
- `EMAIL_HOST_PASSWORD` = `********`
- `AWS_ACCESS_KEY_ID` = `********`
- `AWS_SECRET_ACCESS_KEY` = `********`
- `DATABASE_URL` = `postgres://***:*****@pg.com:5432/***`


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
