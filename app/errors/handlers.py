# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Module of error handlers."""

from flask import render_template

from app import db
from . import bp


@bp.app_errorhandler(404)
def not_found_error(_error):
    """Handle not found error."""
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(_error):
    """Handle internal error."""
    db.session.rollback()
    return render_template('errors/500.html'), 500
