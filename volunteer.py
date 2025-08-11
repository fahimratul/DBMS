import functools
import re
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g
)
from mysql.connector import IntegrityError

from flaskr.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('volunteer', __name__, url_prefix='/volunteer')

def donate():
    render_template('volunteer/volunteer_dashboard.html')