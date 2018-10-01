# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Module of main routes."""

from datetime import date as date_t, datetime
from flask import render_template, redirect, url_for, jsonify

from app import db, models
from . import bp, forms


@bp.route('/index')
@bp.route('/')
def index():
    """Handle root route."""
    query = db.session.query(models.TimePoint.id)
    query = query.order_by(models.TimePoint.id.desc())
    last_time, = query.first()

    query = db.session.query(models.Category)
    query = query.join(models.Sensor)
    query = query.join(models.Data)
    query = query.filter(models.Category.time_id == last_time)
    query = query.filter(models.Sensor.time_id == last_time)
    query = query.filter(models.Sensor.enabled == True)
    query = query.filter(models.Data.time_id == last_time)
    query = query.order_by(models.Category.name)
    query = query.order_by(models.Sensor.name)
    query = query.options(
        db.contains_eager(models.Category.sensors)
        .contains_eager(models.Sensor.datas)
    )
    records = query.all()

    result = []
    for record in records:
        category = record.to_json()
        category['sensors'] = []
        for sensor in record.sensors:
            temp = sensor.to_json()
            temp['value'] = sensor.datas[-1].value
            category['sensors'].append(temp)
        result.append(category)

    return render_template(
        'index.html',
        title='Home',
        main_index='active',
        time=last_time,
        data=result,
    )


@bp.route('/today')
def today():
    """Handle charts route."""
    query = db.session.query(models.DatePoint.id)
    query = query.order_by(models.DatePoint.id.desc())
    dest, = query.first()
    # dest = str(record)
    print(dest)
    return render_template(
        'charts.html',
        title='Today\'s data',
        main_today='active',
        dest=dest,
    )


@bp.route('/edit')
def edit():
    """Handle sensors route."""
    sensor_form = forms.SensorForm()
    category_form = forms.CategoryForm()
    query = db.session.query(models.Category)
    query = query.join(models.Sensor)
    query = query.order_by(models.Category.name)
    query = query.order_by(models.Sensor.name)
    query = query.options(db.contains_eager(models.Category.sensors))
    records = query.all()

    result = []
    for record in records:
        category = record.to_json()
        category['sensors'] = [sensor.to_json() for sensor in record.sensors]
        result.append(category)
    return render_template(
        'edit.html',
        title='Edit',
        main_edit='active',
        data=result,
        sensor_form=sensor_form,
        category_form=category_form,
    )


@bp.route('/edit/sensor', methods=('POST',))
def edit_sensor():
    """Handle edit route."""
    form = forms.SensorForm()
    print(form.enabled.data)
    print(form.enabled.default)

    if form.validate_on_submit():
        sensor = db.session.query(models.Sensor).get(int(form.id.data))

        if (sensor.name == form.name.data
                and sensor.description == form.description.data
                and sensor.enabled == form.enabled.data):
            return jsonify({
                'name': 'Data is not changed.',
                'description': 'Data is not changed.',
                'enabled': 'Data is not changed.',
            })
        sensor.name = form.name.data
        sensor.description = form.description.data
        sensor.enabled = form.enabled.data
        db.session.commit()
        return jsonify({
            'name': form.name.data,
            'description': form.description.data,
            'enabled': form.enabled.data,
            'success': 'Success.'
        })
    return jsonify(form.errors)


@bp.route('/edit/category', methods=('POST',))
def edit_category():
    """Handle edit route."""
    form = forms.CategoryForm()

    if form.validate_on_submit():
        category = db.session.query(models.Category).get(int(form.id.data))

        if (category.name == form.name.data
                and category.measure == form.measure.data
                and category.description == form.description.data
                and category.enabled == form.enabled.data):
            return jsonify({
                'name': 'Data is not changed.',
                'measure': 'Data is not changed.',
                'description': 'Data is not changed.',
                'enabled': 'Data is not changed.',
            })
        old = category.name
        category.name = form.name.data
        category.measure = form.measure.data
        category.description = form.description.data
        category.enabled = form.enabled.data
        db.session.commit()
        return jsonify({
            'name': form.name.data,
            'measure': form.measure.data,
            'description': form.description.data,
            'enabled': form.enabled.data,
            'success': 'Success.',
            'old': old,
        })
    return jsonify(form.errors)


@bp.route('/archive', methods=('GET', 'POST'))
def archive():
    """Handle archive route."""
    form = forms.CalendarForm()
    if form.validate_on_submit():
        return redirect(url_for('main.archive_date', date=str(form.date.data)))

    first_date, = db.session.query(models.DatePoint.id).first()

    query = db.session.query(models.DatePoint.id)
    query = query.order_by(models.DatePoint.id.desc())
    records = query.limit(7).all()
    last_date = records[0][0]

    data = [item[0].isoformat() for item in records]
    return render_template(
        'archive.html',
        title='Archive',
        main_archive='active',
        data=data,
        date_max=str(last_date),
        date_min=str(first_date),
        form=form,
    )


@bp.route('/archive/<date>')
def archive_date(date):
    """Handle archive route."""
    return render_template(
        'charts.html',
        title='Archive data',
        main_archive='active',
        dest=date_t.fromisoformat(date),
    )


@bp.route('/time')
def time():
    """Handle time route."""
    return render_template(
        'new.html',
        text='Now is:',
        date=datetime.now(),
        utc=datetime.utcnow(),
    )
