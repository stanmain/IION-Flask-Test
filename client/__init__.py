# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Package of client IION-Monitor."""


from app import models
from config import Config


def create_app():
    """Create application."""
    from client.main import Client
    return Client(Config())
