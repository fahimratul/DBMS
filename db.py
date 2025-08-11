from os import error
from mysql.connector import connect
from flask import current_app, g
import click

def get_bd():
    if 'db' not in g:
        try:
            g.db = connect(
                host=current_app.config['DATABASE']['host'],
                user=current_app.config['DATABASE']['user'],
                password=current_app.config['DATABASE']['password'],
                database=current_app.config['DATABASE']['database'],
                auth_plugin='mysql_native_password'
            )
            print("Connected to database.")
        except Exception as e:
            g.db = None
            print(f"Database connection error: {e}")
            raise ConnectionError(f"Failed to connect to database: {e}")
        # if i write b instead of d again, i will punch my self

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        if error:
            db.rollback()
        db.close()

def init_db():
    db = get_bd()
    cursor = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        schema = f.read().decode('utf8')
        cursor.execute(schema)

    db.commit()
    cursor.close()
    print("Database initialized.")

@click.command('init-db')
def init_db_command():
    """Command to initialize the database."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

