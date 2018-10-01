# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Models of the application database."""

import json
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base


Model = declarative_base()


def create_all(engine):
    """Create all models."""
    Model.metadata.create_all(engine)


class JsonReprMixin:
    """Add __repr__() from to_json()."""

    def __repr__(self):
        """Return repr."""
        return '<{}({})>'.format(
            self.__class__.__name__,
            json.dumps(self.to_json(), ensure_ascii=False)
        )


class Node(JsonReprMixin, Model):
    """Node model."""

    __tablename__ = 'nodes'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    ref = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(128), default='')
    enabled = db.Column(db.Boolean(), default=True)

    time_id = db.Column(db.DateTime(), db.ForeignKey('timepoints.id'))

    sensors = db.orm.relationship(
        'Sensor', backref='node')

    def to_json(self):
        """Return category in json format."""
        return {
            'id': self.id,
            'name': self.name,
            'ref': self.ref,
            'description': self.description,
            'enabled': self.enabled,
            'time_id': str(self.time_id),
        }


class Category(JsonReprMixin, Model):
    """Category model."""

    __tablename__ = 'categorys'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    measure = db.Column(db.String(16), default='point')
    description = db.Column(db.String(128), default='')
    enabled = db.Column(db.Boolean(), default=True)

    time_id = db.Column(db.DateTime(), db.ForeignKey('timepoints.id'))

    sensors = db.orm.relationship(
        'Sensor', backref=__tablename__
        # lazy='dynamic'
    )

    def to_json(self):
        """Return category in json format."""
        return {
            'id': self.id,
            'name': self.name,
            'measure': self.measure,
            'description': self.description,
            'enabled': self.enabled,
            'time_id': str(self.time_id),
        }


class Sensor(JsonReprMixin, Model):
    """Sensor model."""

    __tablename__ = 'sensors'
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(16), unique=True, index=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(128), default='')
    enabled = db.Column(db.Boolean(), default=True)

    category_id = db.Column(db.Integer(), db.ForeignKey('categorys.id'))
    node_id = db.Column(db.Integer(), db.ForeignKey('nodes.id'))
    time_id = db.Column(db.DateTime(), db.ForeignKey('timepoints.id'))

    datas = db.orm.relationship(
        'Data', backref=__tablename__
        # lazy='dynamic'
    )

    def to_json(self):
        """Return sensor in json format."""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'enabled': self.enabled,
            'category_id': self.category_id,
            'node_id': self.node_id,
            'time_id': str(self.time_id),
        }


class Data(JsonReprMixin, Model):
    """Data model."""

    __tablename__ = 'datas'
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.Float())

    sensor_id = db.Column(db.Integer(), db.ForeignKey('sensors.id'))
    time_id = db.Column(db.DateTime(), db.ForeignKey('timepoints.id'))

    def to_json(self):
        """Return data in json format."""
        return {
            'id': self.id,
            'value': self.value,
            'sensor_id': self.sensor_id,
            'time_id': str(self.time_id),
        }


class TimePoint(JsonReprMixin, Model):
    """Data time model."""

    __tablename__ = 'timepoints'
    id = db.Column(db.DateTime(), primary_key=True)

    date_id = db.Column(db.Integer(), db.ForeignKey('datepoints.id'))

    datas = db.orm.relationship('Data', backref=__tablename__)

    def to_json(self):
        """Return timepoint in json format."""
        return {
            'id': str(self.id),
            'date_id': str(self.date_id),
        }


class DatePoint(JsonReprMixin, Model):
    """Data date model."""

    __tablename__ = 'datepoints'
    id = db.Column(db.Date(), primary_key=True)

    times = db.orm.relationship('TimePoint', backref=__tablename__)

    def to_json(self):
        """Return datepoint in json format."""
        return {
            'id': str(self.id),
        }
