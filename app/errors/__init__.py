# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Package of errors."""

from flask import Blueprint


bp = Blueprint('errors', __name__)


from . import handlers
