# flask db init
# flask db migrate -m "message"
# flask db upgrade


from datetime import date, datetime

from app import create_app, db, models


def main():
    print('Begin')

    app = create_app()
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    add()
    get()
    remove()

    db.session.remove()
    db.drop_all()

    print('End')


def add():
    try:
        print('Adding')

        print('Categorys...')
        category1 = models.Category(
            name='Температура',
            description='Первая категория',
            measure='C',
            last_change=datetime.now())

        category2 = models.Category(
            name='Энергопотребление',
            description='Вторая категория',
            measure='Вт',
            last_change=datetime.now())

        db.session.add(category1)
        db.session.add(category2)
        db.session.commit()

        print('Sensors...')
        sens1 = models.Sensor(
            code='0001',
            name='First',
            description='First sensor',
            category_id=category1.id,
            last_change=datetime.now()
        )

        sens2 = models.Sensor(
            code='0002',
            name='Second',
            description='Second sensor',
            category_id=category2.id,
            last_change=datetime.now()
        )

        db.session.add(sens1)
        db.session.add(sens2)
        db.session.commit()

        print('Dates...')
        today = models.Date(
            value=date.today())

        db.session.add(today)
        db.session.commit()

        print('Datas...')
        data1 = models.Data(
            date_id=today.id,
            time=datetime.now().time(),
            value=25,
            sensor_id=sens1.id
        )

        data2 = models.Data(
            date_id=today.id,
            time=datetime.now().time(),
            value=23,
            sensor_id=sens1.id
        )

        data3 = models.Data(
            date_id=today.id,
            time=datetime.now().time(),
            value=21,
            sensor_id=sens2.id
        )

        db.session.add(data1)
        db.session.add(data2)
        db.session.add(data3)
        db.session.commit()
        print('Compleate')
    except Exception as e:                              # pylint: disable=W0703
        print('Fail')
        print(e)
        db.session.rollback()


def get():
    try:
        print('Categorys:')
        categorys = models.Category.query.all()
        for item in categorys:
            print(item.id, item.name, item.measure,
                  item.description, item.last_change)

        print('Sensors:')
        sensors = models.Sensor.query.all()
        for item in sensors:
            print(item.id, item.code, item.name,
                  item.description, item.last_change)

        print('Dates:')
        dates = models.Date.query.all()
        for item in dates:
            print(item.id, item.value)

        print('Datas:')
        datas = models.Data.query.all()
        for item in datas:
            print(item.id, item.time, item.sensor_id, item.value, item.date_id)
    except Exception as e:                              # pylint: disable=W0703
        print('Fail')
        print(e)


def remove():
    try:
        print('Remove')
        for item in models.Data.query.all():
            db.session.delete(item)

        for item in models.Date.query.all():
            db.session.delete(item)

        for item in models.Sensor.query.all():
            db.session.delete(item)

        for item in models.Category.query.all():
            db.session.delete(item)

        db.session.commit()
        print('Compleate')
    except Exception as e:                              # pylint: disable=W0703
        print('Fail')
        print(e)
        db.session.rollback()


if __name__ == '__main__':
    main()
