# translink-walksheds

An application that allows you to visualize areas within walking distance of public transit stops in Greater Vancouver. I'm currently working on ways to make the walking area accurate; it currently shows reachable areas as the bird flies, but people obviously don't fly. They walk on roads and pathways.

First, install pipenv

Then, in project root:
```shell
pipenv shell
pipenv install
```
then, in project root:
```shell
python manage.py migrate
```

to start the dev server, run:
```shell
python manage.py runserver
```

![Screenshot 1](screenshots/Translink-Walksheds-Google-Chrome-2019-06-20-15-00-06.gif?raw=true "Optional Title")

