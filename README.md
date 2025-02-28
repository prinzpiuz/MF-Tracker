# MF Tracker

Assignment project for [BHIVE Workspace](https://bhiveworkspace.com/)

* To Run the project locally
  * Create a virtual environment and activate it
    `python3.10 -m venv ~/venvs/bhive_project`
    then
    `source ~/venvs/bhive_project/bin/activate`
  * Copy the .env.example to .env and update the values
  `cp dotenv.example .env`
  * Install the requirements.txt
    `pip install -r requirements.txt`
  * Run migrations
    `python manage.py migrate`
  * Run the server
    `python manage.py runserver`

* To Run the project on docker
  * Build the docker
  `docker build`
  * Run the container
  `docker-compose up`
  * To run migrations
  `docker-compose exec web python manage.py migrate`

* API Collection
  [Hoppscotch](https://hoppscotch.io/) / [Postman](https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-from-hoppscotch/) importable collection from [here](./bhive.json)
* Swagger API documentation
  [Swagger](http://127.0.0.1:8000/swagger/)
