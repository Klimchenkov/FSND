# Udacity Full-Stack Nanodegree: Capstone Project

## Content

1. [Motivation for the project](#motivation)
2. [URL location for the hosted API](#URL)
3. [Deploy and run the project locally](#Local_run)
4. [API documentation](#API)
5. [Testing](#tests)
6. [Authentication and RBAC controls](#RBAC)

<a name="motivation"></a>

## Motivation for the project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The Executive Producer of company wants to create a system to simplify and streamline the working process.

<a name="URL"></a>

## URL location for the hosted API

You can access the hosted API of the project through this link https://casting-klimchenkov.herokuapp.com

<a name="Local_run"></a>

## Deploy and run the project locally

To get started, make sure you cd into the project directory and proceed with the following steps to set it up. To run the application, you will need the latest version of Python 3 and running PostgreSQL server. It is recomended that you initialize and activate a virtualenv in the projects directory. 

1. Initialize and activate a virtualenv:

```bash
python -m virtualenv env
. env/Scripts/activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Set the enviroment variables. Envs are stored in the setup.sh file. It sets database configuration and credentials and also sets AUTH0 connection details and bearer tokens for RBAC. You may need to change database variables to access your local database server. You may also need to change commands to set the `envs`, as they are given for `git bash for Windows`.

- Open `setup.sh` with your editor of choice
- Find global variable with the name `DATABASE_URL`:

```bash
export DATABASE_URL="postgresql://postgres:abc@localhost:5432/casting"
```
Where the following syntax is followed: 

```bash
DATABASE_URL = "postgres://{username}:{password}@{host_and_port}/{database_name}"
```
- change `username`, `password` and `host_and_post` to those you've chosen while installing PostgreSQL. 
- you may also need to change global password and user to access your Postgres server:
```bash
$ export PGUSER=postgres
$ export PGPASSWORD=abc
```
- run `setup.sh` script in your bash:
```bash
$ . setup.sh
```
4. Run the development server on http://localhost:5000/:
```bash
$ python app.py
```

<a name="API"></a>

## API documentation

Here you can find details of all existing endpoints of the application. Existing endpoints are:

- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

### GET '/api/v1.0/movies' 

- Fetches details of all existing movies, including title and release date. 
- Returns list of movies and boolean 'Success'

Example response:
```json
{
    "Movies": [
        {
            "ID": 1,
            "Release date": "Wed, 14 Dec 1988 00:00:00 GMT",
            "Title": "Rain man"
        },
        {
            "ID": 2,
            "Release date": "Wed, 22 May 1996 00:00:00 GMT",
            "Title": "Mission impossible"
        }, ...
        ],
    "Success": true
}
```

### GET '/api/v1.0/actors' 

- Fetches details of all existing actors, including name, age and gender. 
- Returns list of movies and boolean 'Success'

Example response:
```json
{
    "Actors": [
        {
            "Age": 52,
            "Gender": "Male",
            "ID": 1,
            "Name": "Matt Daemon"
        },
        {
            "Age": 53,
            "Gender": "Male",
            "ID": 2,
            "Name": "Matthew McConaughey"
        },...
    ],
    "Success": true
}
```

### POST '/api/v1.0/movies' 

- Sends a post request in order to add a new movie
- Request Body:

```json
{
    "Release date": "Some release date in yyyy.mm.dd format",
    "Title": "Some title of the movie"
}
```

### POST '/api/v1.0/actors' 

- Sends a post request in order to add a new actor
- Request Body:

```json
{
    "Age": "Some actors age",
    "Gender": "Some actors gender",
    "Name": "Some actors name"
}
```

### DELETE '/api/v1.0/movies/${id}'

- Deletes a specified movie using the id of the movie
- Request Arguments: id - integer
- Returns: Appropriate HTTP status code and the id of the deleted movie


### DELETE '/api/v1.0/actors/${id}'

- Deletes a specified actor using the id of the actor
- Request Arguments: id - integer
- Returns: Appropriate HTTP status code and the id of the deleted actor

### PATCH '/api/v1.0/movies/${id}'

- Edit an existing Movie information
- Request Arguments: id - integer
- Request Headers (application/json)   
```json
{
    "Release date(optional)": "Some release date in yyyy.mm.dd format",
    "Title(optional)": "Some title of the movie"
}
```
- Returns: Appropriate HTTP status and updated movie details.
- Example response:
```json
{
    "Movie": {
        "ID": "Some movie ID",
        "Release date": "Some movie release date",
        "Title": "Some movie title"
    },
    "Success": true
}
```

### PATCH '/api/v1.0/actors/${id}'

- Edit an existing Actor information
- Request Arguments: id - integer
- Request Headers (application/json)   

```json
{
    "Age(optional)": "Some actors age",
    "Gender(optional)": "Some actors gender",
    "Name(optional)": "Some actors name"
}
```
- Returns: Appropriate HTTP status and updated actor details.
- Example response:
```json
{
    "Actor": {
        "Age": "Some actors age",
        "Gender": "Some actors gender",
        "ID": "Some actors ID",
        "Name": "Some actors name"
    },
    "Success": true
}
```

<a name="tests"></a>
## Testing

To run the tests: 
- Navigate to projects directory
- Make sure you have Postgres server running
- Make sure you've already ran the setup.sh script, which set the actual bearer tokens for the existing roles
- Run the `test_db_setup.sh` script, it will create and populate casting_test database from the casting_test.sql file:
```bash
$ . test_db_setup.sh
```
- Run the test_app.py:
```bash
$ python test_app.py
```
- It will run 6 test for RBAC behaviour and 16 test for endpoints, both for success and errors.
- After running the tests, you should get the following response:
```python
$ python test_app.py
----------------------------------------------------------------------
Ran 22 tests in 26.123s

OK
```
<a name="RBAC"></a>
## Authentication and RBAC controls
There are 3 existing roles with special permissions:

- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

You can find actual tokens for each of this role in the `setup.sh` file. Actual tokens are set up as enviromental variables. To access endpoints of the running app you can run curl commands in your `bash`. Make sure you run `setup.sh` script first. 

For example, to access `/movies` endpoint in the role of casting_assistant_token run the following command:
``` bash
curl https://casting-klimchenkov.herokuapp.com/movies -H "Authorization: $casting_assistant_token"
```
You should get the following response:
```bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   662  100   662    0     0    643      0  0:00:01  0:00:01 --:--:--   645{"Movies":[{"ID":2,"Release date":"Wed, 22 May 1996 00:00:00 GMT","Title":"Mission impossible"},{"ID":3,"Release date":"Fri, 14 Dec 2001 00:00:00 GMT","Title":"Vanilla Sky"},{"ID":4,"Release date":"Wed, 11 Dec 1996 00:00:00 GMT","Title":"Jerry Maguire"},{"ID":5,"Release date":"Sat, 08 Dec 2018 00:00:00 GMT","Title":"Icebox"},{"ID":6,"Release date":"Fri, 04 Mar 2022 00:00:00 GMT","Title":"The Batman"},{"ID":8,"Release date":"Fri, 09 Jan 1998 00:00:00 GMT","Title":"Good Will Hunting"},{"ID":9,"Release date":"Fri, 15 Nov 2019 00:00:00 GMT","Title":"Ford vs Ferrari"},{"ID":1,"Release date":"Thu, 13 Jan 2000 00:00:00 GMT","Title":"Rain man"}],"Success":true}
```


