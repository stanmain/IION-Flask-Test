# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Module of main forms."""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, InputRequired


class CalendarForm(FlaskForm):
    """Calendar form."""

    date = DateField(label='Выберите дату:', validators=(DataRequired(),))
    # submit = SubmitField('Выбрать')


class SensorForm(FlaskForm):
    """Sensor form."""

    id = HiddenField(validators=(InputRequired(),))
    name = StringField(validators=(InputRequired(), Length(min=4, max=32)))
    description = StringField(validators=(InputRequired(), Length(max=256)))
    enabled = BooleanField()


class CategoryForm(FlaskForm):
    """Sensor form."""

    id = HiddenField(validators=(InputRequired(),))
    name = StringField(validators=(InputRequired(), Length(min=4, max=32)))
    measure = StringField(validators=(InputRequired(), Length(min=1, max=16)))
    description = StringField(validators=(InputRequired(), Length(max=256)))
    enabled = BooleanField()
