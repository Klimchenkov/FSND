# Udacity Full-Stack Nanodegree: Capstone Project

## Content

1. [Motivation for the project](#motivation)
2. [URL location for the hosted API](#URL)
3. [Deploy and run the project locally](#Local_run)

<a name="motivation"></a>

##Motivation for the project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The Executive Producer of company wants to create a system to simplify and streamline the working process.

<a name="URL"></a>

## URL location for the hosted API

You can access the hosted API of the project through this link https://casting-klimchenkov.herokuapp.com/movies

<a name="Local_run></a>

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

3. Set the enviroment variables. Envs are stored in the setup.sh file. It sets database configuration and credentials and also sets AUTH0 connection details and bearer tokens for RBAC. You may need to change database variables to access your local database server. You also may need to change commands to set the `envs`, as they are given for `git bash for Windows`.

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







