# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Main package."""

from flask import Blueprint


bp = Blueprint('main', __name__)


from . import views
