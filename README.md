# docker-django-react

Blank Project for ticket sniping, with django/react and postgres

## Prerequisites

### Docker

1. Docker
1. docker-compose

## Installation

### Docker

1. Navigate to the repo directory : `cd your-project-name`
1. Execute `docker-compose up`.
1  Wait until the build has finished, this may take 15-20 mins on the first build, but will be near instant on subsequent builds.
1. Once build has finished, the containers will be running on ports : backend:8000, frontend:3000/8101, database:5432, scraping:1234
1. There is a proxy running so that all backend requests @ port 8000 automatically direct to the front end localhost:8101, which shows the website

## Working with Containers 
1. To execute any command on a container : docker-compose exec <container> <command>, for example: docker-compose exec scraping python main.py, executes a python script 'main.py' on the scraping container.
2. running docker-compose exec <container> sh, will open a shell in the container - ONLY use in debugging purposes
3. all containers track files in their respective folders, everything edited in the /frontend folder will be automatically shared with the container, so there is no need to rebuild or sh into the container.
4. when you want to shut down the containers, use docker-compose down.

### Database
1. database settings (db name, db login etc) are in the .env file in the project root, used mainly for init reasons only (note that if you want do a FULL delete an remake of the database you will need to run docker-compose down -v and get rid of the database/local_volume/pgdata folder )
1. The contents of the database/ folder is mainly docker init files, and volumes where the database data is backed up, if you want to access the database tables you will need to run an exec command on the container. (assuming default username, db) docker-compose exec database psql --username dev --dbname=snipe_data_dev

### Scraping
1. all scraping files are linked to the container via the scraping/ folder. Note that the scraping container is built to use the chromedriver_binary python package.
1. to test a script run: docker-compose exec scraping python main.py
1. to enter files into the database, remember that the database is running on localhost:5432

### Backend
1. to access the django back-end go to localhost:8000/admin, note that going to localhost:8000 alone will redirect you straight to the front end of the site.
1. to create a new django superuser, run docker-compose exec backend python manage.py createsuperuser, same with other django commands of collectstatic, migrate, makemigrations etc.
1. default superuser should be u:admin p:admin
1. django settings are in the backend/core/ folder, and the site build is in the backend/sniping_site/ folder
1. the frontend and backend are connected with the REST framework. going to localhost:8000/api/ will show the current data being serialised/served

### Frontend
1. front end and back end are connected through a proxy in the package.json file, data is served via the REST framework and axios.
1. front end static files are all located in frontend/src/
 
### REMAINING ISSUES
1. some teething problems with volumes, if there are indiscriminate volumes dangling around that are clogging up your machine, check with docker volume ls and use docker volume rm etc
1. builds are still long and need to be optimised, i'm still commiting all the packages and volumes to github which really isn't ideal, need to look over this once the basic functionality is up.









