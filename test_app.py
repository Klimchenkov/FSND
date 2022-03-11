import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Actor, Movie, setup_db

casting_assistant_token = os.environ['casting_assistant_token']
casting_director_token = os.environ['casting_director_token']
executive_producer_token = os.environ['executive_producer_token']

casting_assistant_auth_header = {
    'Authorization': casting_assistant_token
}

casting_director_auth_header = {
    'Authorization': casting_director_token
}

executive_producer_auth_header = {
    'Authorization': executive_producer_token
}

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass

    #tests for expected success and error behavior for each endpoint

    ''' 
        GET movies
        two tests, one for success and one for the missing authorization header
    '''

    def test_get_movies(self):
        res = self.client().get('/movies', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_error_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    ''' 
        GET actors
        two tests, one for success and one for the missing authorization header
    '''

    def test_get_actors(self):
        res = self.client().get('/actors', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_error_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    '''
        POST movie
        two tests, one for success and one for the missing data
    '''

    def test_post_a_movie(self):
        json_new_movie = {
            'title': 'From Dusk till Dawn',
            'release_date': '1996.01.19'  
        }
        res = self.client().post('/movies', json=json_new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_error_missing_data_new_movie(self):
        json_new_movie = {
            'title': 'From Dusk till Dawn' 
        }

        res = self.client().post('/movies', json=json_new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Unprocessable Entity")

    '''
        POST actor
        two tests, one for success and one for the missing data
    '''

    def test_post_an_actor(self):
        json_new_actor = {
            'name': 'George Clooney',
            'age': '60',
            'gender': 'Male'
        }
        res = self.client().post('/actors', json=json_new_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_error_missing_data_new_actor(self):
        json_new_actor = {
            'name': 'George Clooney',
            'age': '60'
        }

        res = self.client().post('/actors', json=json_new_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Unprocessable Entity")

    '''
        PATCH movie
        two tests, one for success and one for failed attempt to change movie that does not exist in the database
    '''

    def test_change_movie(self):
        json_change_movie_release_date = {
            'release_date': '2000.01.19'  
        }
        res = self.client().patch('/movies/1', json=json_change_movie_release_date, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['Success']) 

    def test_error_change_movie_that_not_exist(self):
        json_change_movie_release_date = {
            'release_date': '2000.01.19'  
        }
        res = self.client().patch('/movies/100000000', json=json_change_movie_release_date, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Resource Not Found")

    '''
        PATCH actor
        two tests, one for success and one for failed attempt to change actor that does not exist in the database
    '''

    def test_change_actor(self):
        json_change_actors_age = {
            'age': '50'  
        }
        res = self.client().patch('/actors/1', json=json_change_actors_age, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['Success']) 

    def test_error_change_actor_that_not_exist(self):
        json_change_actors_age = {
            'age': '50'   
        }
        res = self.client().patch('/actors/100000000', json=json_change_actors_age, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Resource Not Found")

    '''
        DELETE movie
        two tests, one for success and one for failed attempt to delete movie that does not exist
    '''
    
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_delete_movie_that_not_exist(self):
        res = self.client().delete('/movies/10000000', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Resource Not Found")

    '''
        DELETE actor
        two tests, one for success and one for failed attempt to delete actor that does not exist
    '''
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_delete_actor_that_not_exist(self):
        res = self.client().delete('/actors/10000000', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Resource Not Found")

    #tests demonstrating role-based access control, two per each role

    '''
        Casting assistant role
        can GET movies but cannot POST them
    '''
    def test_casting_assistant_get_movies(self):
        res = self.client().get('/movies', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success']) 

    def test_casting_assistant_post_a_movie(self):
        json_new_movie = {
            'title': 'From Dusk till Dawn',
            'release_date': '1996.01.19'  
        }
        res = self.client().post('/movies', json=json_new_movie, headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

    '''
        Casting director role
        Can POST an actor but cannot POST a movie
    '''
    def test_casting_director_post_an_actor(self):
        json_new_actor = {
            'name': 'George Clooney',
            'age': '60',
            'gender': 'Male'
        }
        res = self.client().post('/actors', json=json_new_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_casting_director_post_a_movie(self):
        json_new_movie = {
            'title': 'From Dusk till Dawn',
            'release_date': '1996.01.19'  
        }
        res = self.client().post('/movies', json=json_new_movie, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

    '''
    Executive producer role
    can do anything he wants
    '''
    def test_executive_producer_post_an_actor(self):
        json_new_actor = {
            'name': 'George Clooney',
            'age': '60',
            'gender': 'Male'
        }
        res = self.client().post('/actors', json=json_new_actor, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])
    
    def test_executive_producer_post_a_movie(self):
        json_new_movie = {
            'title': 'From Dusk till Dawn',
            'release_date': '1996.01.19'  
        }
        res = self.client().post('/movies', json=json_new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])


if __name__ == "__main__":
    unittest.main()