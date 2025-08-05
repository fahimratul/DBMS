from flask import Flask
import os

def create_app(test_config=None):
    #create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = {
            'host':'localhost',
            'user':'flaskuser',
            'password':'flask',
            'database':'donation' #the name of the database, do not get confused with DATABASE map
        }
    )

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #otherwise load the test config that has been passed to create_app() function
        app.config.from_mapping(
            test_config
        )

    #make sure the instance folder exists
    #this is improtant as all configuration 
    #files are relative to instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # TURN DEBUGING OFF BEFORE LAUNCING
    app.config['DEBUG'] = True

    #register the databse connection
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    #dummy page saying hello
    @app.route('/')
    def index():
        return 'hello  world!'
    
    return app