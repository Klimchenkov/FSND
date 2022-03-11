import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  #ROUTES

  '''
      GET /movies endpoint
      it requires the 'get:movies' permission
      it contains Movie data representation
      returns status code 200 and json {"success":True, "Movies": movies} where movies is the 
      list of movies or appropriate status code indicating reason for failure
  '''

  @app.route('/movies', methods=['GET'])
  @requires_auth(permission='get:movies')
  def get_movies(payload):
    try:
      movies = Movie.query.all()
      return jsonify({"Success":True, "Movies": [movie.format() for movie in movies]}), 200
    except:
      abort(404)


  '''
      GET /actors endpoint
      it requires the 'get:actprs' permission
      it contains Actor data representation
      returns status code 200 and json {"success":True, "Actors": actors} where actors is the 
      list of actors or appropriate status code indicating reason for failure
  '''

  @app.route('/actors', methods=['GET'])
  @requires_auth(permission='get:actors')
  def get_actors(payload):
    try:
      actors = Actor.query.all()
      return jsonify({"Success":True, "Actors": [actor.format() for actor in actors]}), 200
    except:
      abort(404)

  '''
    POST /movies endpoint
    it creates a new row in the drinks table
    it requires the 'change:movies' permission
    returns status code 200 and json {"success":True, "movie": movie} where movie is an array containing only the newly
    created movie or appropriate status code indicationg reacon for failure
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth(permission='change:movies')
  def post_a_movie(payload):
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    try:
      if title and release_date:
        movie = Movie(title = title, release_date = release_date)
        movie.insert()
        return jsonify({
          "Success": True,
          "Movie": movie.format()
        }), 200
      else:
        abort(422)
    except Exception as e:
      print(e)
      abort(422)

  ''' 
    POST /actors endpoint
    it creates a new row in the actors table
    it requires the 'change:actors' permission
    returns status code 200 and json {"success":True, "Actor": actor} where actor is an array containing only the newly
    created actor or appropriate status code indicationg reacon for failure
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth(permission='change:actors')
  def post_an_actor(payload):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    try:
      if name and age and gender:
        actor = Actor(name = name, age = age, gender = gender)
        actor.insert()
        return jsonify({
          "Success": True,
          "Actor": actor.format()
        }), 200
      else:
        abort(422)
    except Exception as e:
      print(e)
      abort(422)

  '''
    PATCH /movies/<id> endpoint
      where <id> is the existing model id
      it respond with a 404 error if <id> is not found
      it updates the corresponding row for <id>
      it requires 'change:movies' perission
      it contains the movie data representation
      returns status code 200 and json {"success": True, "movie": movie} where movie is an array containing only the updated 
      movie or appropriate status code indicating reason for failure
  '''
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth(permission='change:movies')
  def change_movie(payload, movie_id):
    movie = Movie.query.get_or_404(movie_id)
    body = request.get_json() 
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    try:
      if title:
        movie.title = title
      if release_date:
        movie.release_date = release_date

      movie.update()
      return jsonify({
        "Success": True,
        "Movie": movie.format()
      }), 200
    except Exception as e:
      print(e)
      abort(422)

  '''
    PATCH /actors/<id> endpoint
      where <id> is the existing model id
      it respond with a 404 error if <id> is not found
      it updates the corresponding row for <id>
      it requires 'change:actors' perission
      it contains the actor data representation
      returns status code 200 and json {"success": True, "actor": actor} where actor is an array containing only the updated 
      actor or appropriate status code indicating reason for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth(permission='change:actors')
  def change_actor(payload, actor_id):
    actor = Actor.query.get_or_404(actor_id)
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    try:
      if name:
        actor.name = name
      if age:
        actor.age = age
      if gender:
        actor.gender = gender

      actor.update()
      return jsonify({
        "Success": True,
        "Actor": actor.format()
      }), 200
    except Exception as e:
      print(e)
      abort(422)
  
  '''
    DELETE /movie/<id> endpoint
    where <id> is the existing model id
    it responds with a 404 error if <id> is nor found
    it deletes the corresponding row for <id>
    it requires the 'change:movies' permission
    returns status code 200 and json ("success": True, "delete": id) where id is the id of the deleted record
    or appropriate status code indicating reason for failure
  '''
  @app.route('/movies/<int:movie_id>', methods = ['DELETE'])
  @requires_auth(permission='change:movies')
  def delete_the_movie(payload, movie_id):
    movie = Movie.query.get_or_404(movie_id)
    try:
      movie.delete()
      return jsonify({
        'Success': True,
        'Delete': movie_id
      }), 200
    except Exception as e:
      print(e)
      abort(422)

  '''
    DELETE /actor/<id> endpoint
    where <id> is the existing model id
    it responds with a 404 error if <id> is nor found
    it deletes the corresponding row for <id>
    it requires the 'change:actors' permission
    returns status code 200 and json ("success": True, "delete": id) where id is the id of the deleted record
    or appropriate status code indicating reason for failure
  '''
  @app.route('/actors/<int:actor_id>', methods = ['DELETE'])
  @requires_auth(permission='change:actors')
  def delete_an_actor(payload, actor_id):
    actor = Actor.query.get_or_404(actor_id)
    try:
      actor.delete()
      return jsonify({
        'Success': True,
        'Delete': actor_id
      }), 200
    except Exception as e:
      print(e)
      abort(422)

  # Error Handling

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request",
          "additional_information": error.description
      }), 400

  @app.errorhandler(404)
  def resource_not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found",
          "additional_information": error.description
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method Not Allowed",
          "additional_information": error.description
      }), 405

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable Entity",
          "additional_information": error.description
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error",
          "additional_information": error.description
      }), 500



  '''
  error handler for AuthError
  ''' 

  @app.errorhandler(AuthError)
  def authentification_failed(AuthError):
    return jsonify({
      "success": False,
      "error": AuthError.status_code,
      "message": AuthError.error['description']
      }), AuthError.status_code


  return app

app = create_app()

if __name__ == '__main__':
    app.run()