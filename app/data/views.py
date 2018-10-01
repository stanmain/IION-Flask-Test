# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Module of data routes."""

from flask import jsonify, request

from app import models, db
from . import bp


@bp.route('/charts/<date>')
def charts(date):
    """Handle today data route."""
    print(request.args.get('tz', '+0000'))
    query = db.session.query(models.DatePoint)
    query = query.join(models.TimePoint)
    query = query.filter(models.DatePoint.id == date)
    query = query.filter(models.TimePoint.date_id == models.DatePoint.id)
    query = query.options(
        db.contains_eager(models.DatePoint.times)
    )
    current_day = query.first_or_404()
    time_records = current_day.times

    query = db.session.query(models.Category)
    query = query.join(models.Sensor)
    query = query.join(models.Data)
    query = query.join(models.TimePoint)
    query = query.filter(models.Sensor.category_id == models.Category.id)
    query = query.filter(models.Data.sensor_id == models.Sensor.id)
    query = query.filter(models.TimePoint.date_id == date)
    query = query.order_by(models.Category.name)
    query = query.order_by(models.Sensor.name)
    query = query.order_by(models.Data.time_id)
    query = query.options(
        db.contains_eager(models.Category.sensors)
        .contains_eager(models.Sensor.datas)
    )
    data_records = query.all()

    result = []

    for category in data_records:
        temp = category.to_json()
        cols = ['X']
        for sensor in category.sensors:
            if sensor.name == '' or sensor.name is None:
                cols.append(sensor.code)
            else:
                cols.append(sensor.name)
        temp['cols'] = cols

        rows = []
        for time in time_records:
            row = [time.id.hour + time.id.minute / 60]
            for sensor in category.sensors:
                value = None
                for data in sensor.datas:
                    if data.time_id == time.id:
                        value = data.value
                        break
                row.append(value)
            rows.append(row)
        temp['rows'] = rows
        result.append(temp)

    return jsonify(
        result
    )


# @bp.route('/charts/<date>')
# def charts(date):
#     """Handle today data route."""
#     query = db.session.query(models.DatePoint.id)
#     query = query.filter(models.DatePoint.id == date)
#     dest, = query.first_or_404()
#     # return jsonify(str(dest))
#     query = db.session.query(
#         models.Data.value,
#         models.Sensor.id, models.Sensor.name,
#         models.Category.id, models.Category.name, models.Category.measure,
#         models.TimePoint.id, models.TimePoint.date_id
#     )
#     query = query.join(models.Sensor)
#     query = query.join(models.Category)
#     query = query.join(models.TimePoint)
#     query = query.filter(models.TimePoint.date_id == dest)
#     records = query.all()
#     data = func.group_category(records)
#     return jsonify(data)


@bp.route('/nearest/<date>')
def nearest(date):
    """Lololo."""
    query = db.session.query(models.DatePoint.id)
    query = query.filter(models.DatePoint.id > date)
    query = query.order_by(models.DatePoint.id)
    records_right = query.limit(3).all()
    data_right = [str(record[0]) for record in records_right]

    query = db.session.query(models.DatePoint.id)
    query = query.filter(models.DatePoint.id < date)
    query = query.order_by(models.DatePoint.id.desc())
    records_left = query.limit(3).all()
    data_left = [*reversed([str(record[0]) for record in records_left])]

    return jsonify({
        'left': data_left,
        'right': data_right,
    })


# @bp.route('/datas')
# def datas_list():
#     """Handle datas list route."""
#     query = db.session.query(
#         models.Data.value, models.Sensor.name, models.Category.name,
#         str(models.Time.value), models.Date.value)
#     query = query.join(models.Sensor)
#     query = query.join(models.Category)
#     query = query.join(models.Time)
#     query = query.join(models.Date)
#     records = query.all()
#     return jsonify(records)


# @bp.route('/dates')
# def dates_list():
#     """Handle dates list route."""
#     items = models.Date.query.all()
#     return jsonify([item.to_json() for item in items])


# @bp.route('/times')
# def times_list():
#     """Handle times list route."""
#     items = models.Time.query.all()
#     return jsonify([item.to_json() for item in items])


# @bp.route('/categorys')
# def categorys_list():
#     """Handle categorys list route."""
#     items = models.Category.query.all()
#     return jsonify([item.to_json() for item in items])


# @bp.route('/sensors')
# def sensors_list():
#     """Handle sensors list route."""
#     items = models.Sensor.query.all()
#     return jsonify([item.to_json() for item in items])
