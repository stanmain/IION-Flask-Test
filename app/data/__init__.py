# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Package of data."""

from flask import Blueprint


bp = Blueprint('data', __name__)


from . import views
