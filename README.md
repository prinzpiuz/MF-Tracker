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

* Command To Update NAV

    ```shell
    python manage.py update_nav
    ```

* To Run the project on docker
  * Build the docker
  `docker build`
  * Run the container
  `docker-compose up`
  * To run migrations
  `docker-compose exec web python manage.py migrate`
  * update the nav
  `docker-compose exec web python manage.py update_nav`

* To run test cases
  `python manage.py test`

* API Collection
  [Hoppscotch](https://hoppscotch.io/) / [Postman](https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-from-hoppscotch/) importable collection from [here](./bhive.json)

* Available Endpoints

  * Create Account `api/v1/create_account/`

    ```shell
    curl --request POST \
    --url http://localhost:8000/api/v1/create_account/ \
    --header 'content-type: application/json' \
    --data '{
    "email": "testuser+7@example.com",
    "password": "testpass123",
    "password_confirmation": "testpass123"

    }
    ```

    Response

    ```json
            {
        "id": 8,
        "email": "<testuser+8@example.com>"
        }
    ```

  * Login `api/v1/login/`

    ```shell
        curl --request POST \
        --url http://localhost:8000/api/v1/login/ \
        --header 'content-type: application/json' \
        --data '{
        "username": "testuser+7@example.com",
        "password": "testpass123"

        }

    ```

    Response

    ```json
        {
            "token": "fa303ca16d5de9811ed121625350b587920af5f6",
            "user_id": 7,
            "username": "testuser+7@example.com"
        }

    ```

  * List Mutual Funds `api/v1/list_mfs/`

    ```shell
    curl --request GET \
    --url http://localhost:8000/api/v1/list_mfs/ \
    --header 'Authorization: Token fa303ca16d5de9811ed121625350b587920af5f6'
    ```

    Response

    ```json
    [
    {
        "Scheme_Code": 120437,
        "ISIN_Div_Payout_ISIN_Growth": "-",
        "ISIN_Div_Reinvestment": "INF846K01CU0",
        "Scheme_Name": "Axis Banking & PSU Debt Fund - Direct Plan - Daily IDCW",
        "Net_Asset_Value": 1038.5219,
        "Date": "28-Feb-2025",
        "Scheme_Type": "Open Ended Schemes",
        "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
        "Mutual_Fund_Family": "Axis Mutual Fund"
    },]
    ```

  * Add Mutual Funds `api/v1/add_fund/`

    ```shell
        curl --request POST \
        --url http://localhost:8000/api/v1/add_fund/ \
        --header 'Authorization: Token 376894d1d346e5aaeaf46231c9a22debdeb62ab3' \
        --header 'content-type: application/json' \
        --data '{"quantity": 600, "scheme_Code": "148633"}'

    ```

    Response

    ```json
    {
    "message": "Funds added successfully"
    }

    ```

  * Portfolio `api/v1/list_portfolio/`

    ```shell
    curl --request GET \
    --url http://localhost:8000/api/v1/list_portfolio/ \
    --header 'Authorization: Token fa303ca16d5de9811ed121625350b587920af5f6'
    ```

    Response

    ```json
    [{
    "id": 5,
    "mf_name": "Axis Innovation Fund - Regular Plan - IDCW",
    "nav": 16.24,
    "quantity": 600,
    "current_value": 9744.0
    }]

    ```
