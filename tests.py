# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Module of tests."""

import unittest
from datetime import datetime, timedelta
from app import create_app, db, models, Config


class TestConfig(Config):
    """Class of tests configuration parameters."""

    pass
    # TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ModelsCase(unittest.TestCase):
    """Testing case."""

    def setUp(self):
        """Set up test case."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        models.create_all(db.engine)
        self.add_data()

    def tearDown(self):
        """Tear down test case."""
        # db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def add_data(self):
        """Add data into db."""
        try:
            self.datetime = datetime.utcnow()
            datepoint1 = models.DatePoint(
                id=self.datetime.date())
            datepoint2 = models.DatePoint(
                id=self.datetime.date() - timedelta(days=1))
            datepoint3 = models.DatePoint(
                id=self.datetime.date() - timedelta(days=2))

            db.session.add(datepoint1)
            db.session.add(datepoint2)
            db.session.add(datepoint3)
            db.session.commit()

            timepoint1 = models.TimePoint(
                id=self.datetime,
                date_id=datepoint1.id
            )
            timepoint2 = models.TimePoint(
                id=self.datetime - timedelta(days=1, hours=2),
                date_id=datepoint2.id
            )
            timepoint3 = models.TimePoint(
                id=self.datetime - timedelta(days=2, hours=5),
                date_id=datepoint3.id
            )

            db.session.add(timepoint1)
            db.session.add(timepoint2)
            db.session.add(timepoint3)
            db.session.commit()

            node1 = models.Node(
                name='Node 1',ref='node1.com', description='Empty',
                enabled=True, time_id=timepoint1.id)
            node2 = models.Node(
                name='Node 2', ref='node2.com', description='Empty',
                enabled=True, time_id=timepoint1.id)

            db.session.add(node1)
            db.session.add(node2)
            db.session.commit()

            cat1 = models.Category(name='Cat 1', measure='AAA', description='Empty', enabled=True, time_id=timepoint1.id)
            cat2 = models.Category(name='Cat 2', measure='AAA', description='Empty', enabled=True, time_id=timepoint1.id)

            db.session.add(cat1)
            db.session.add(cat2)
            db.session.commit()

            sens1 = models.Sensor(name='Sens 1', code='0001', description='Empty', enabled=True, category_id=cat1.id, node_id=node1.id, time_id=timepoint1.id)
            sens2 = models.Sensor(name='Sens 2', code='0002', description='Empty', enabled=True, category_id=cat1.id, node_id=node2.id, time_id=timepoint2.id)
            sens3 = models.Sensor(name='Sens 3', code='0003', description='Empty', enabled=True, category_id=cat2.id, node_id=node1.id, time_id=timepoint1.id)            

            db.session.add(sens1)
            db.session.add(sens2)
            db.session.add(sens3)
            db.session.commit()

            data1 = models.Data(value=17, sensor_id=sens1.id, time_id=timepoint3.id)

            data2 = models.Data(value=14, sensor_id=sens1.id, time_id=timepoint2.id)
            data3 = models.Data(value=15, sensor_id=sens2.id, time_id=timepoint2.id)            
            
            data4 = models.Data(value=13, sensor_id=sens3.id, time_id=timepoint1.id)
            data5 = models.Data(value=12, sensor_id=sens2.id, time_id=timepoint1.id)
            data6 = models.Data(value=11, sensor_id=sens1.id, time_id=timepoint1.id)

            db.session.add(data1)
            db.session.add(data2)
            db.session.add(data3)
            db.session.add(data4)
            db.session.add(data5)
            db.session.add(data6)
            db.session.commit()

        except Exception as e:                          # pylint: disable=W0703
            print('Fail add data.')
            print(e)
            db.session.rollback()

    def test_data(self):
        """Test data."""
        print('Go')
        records = db.session.query(models.DatePoint).all()
        for record in records:
            print(record)

        records = db.session.query(models.TimePoint).all()
        for record in records:
            print(record)

        records = db.session.query(models.Data).all()
        for record in records:
            print(record)

        records = db.session.query(models.Sensor).all()
        for record in records:
            print(record)

        records = db.session.query(models.Category).all()
        for record in records:
            print(record)

        records = db.session.query(models.Node).all()
        for record in records:
            print(record)

    # def test_categorys_data(self):
    #     """Test of categorys data."""
    #     categorys = models.Category.query.all()
    #     with self.subTest('First'):
    #         self.assertEqual(categorys[0].id, 1)
    #         self.assertEqual(categorys[0].name, 'Температура')
    #         self.assertEqual(categorys[0].description, 'Первая категория')
    #         self.assertEqual(categorys[0].measure, 'C')
    #         self.assertEqual(categorys[0].last_change, self.datetime)
    #     with self.subTest('Second'):
    #         self.assertEqual(categorys[1].id, 2)
    #         self.assertEqual(categorys[1].name, 'Энергопотребление')
    #         self.assertEqual(categorys[1].description, 'Вторая категория')
    #         self.assertEqual(categorys[1].measure, 'Вт')
    #         self.assertEqual(categorys[1].last_change, self.datetime)

    # def test_sensors_data(self):
    #     """Test of sensors data."""
    #     sensors = models.Sensor.query.all()
    #     with self.subTest('First'):
    #         self.assertEqual(sensors[0].id, 1)
    #         self.assertEqual(sensors[0].code, '0001')
    #         self.assertEqual(sensors[0].name, 'First')
    #         self.assertEqual(sensors[0].description, 'First sensor')
    #         self.assertEqual(sensors[0].category_id, 1)
    #         self.assertEqual(sensors[0].last_change, self.datetime)
    #     with self.subTest('Second'):
    #         self.assertEqual(sensors[1].id, 2)
    #         self.assertEqual(sensors[1].code, '0002')
    #         self.assertEqual(sensors[1].name, 'Second')
    #         self.assertEqual(sensors[1].description, 'Second sensor')
    #         self.assertEqual(sensors[1].category_id, 2)
    #         self.assertEqual(sensors[1].last_change, self.datetime)

    # def test_dates_data(self):
    #     """Test of dates data."""
    #     date = models.Date.query.first()
    #     self.assertEqual(date.id, 1)
    #     self.assertEqual(date.value, self.datetime.date())

    # def test_times_data(self):
    #     """Test of times data."""
    #     time = models.Time.query.first()
    #     self.assertEqual(time.id, 1)
    #     self.assertEqual(time.value, self.datetime.time())

    # def test_datas_data(self):
    #     """Test of datas data."""
    #     datas = models.Data.query.all()
    #     with self.subTest('First'):
    #         self.assertEqual(datas[0].id, 1)
    #         self.assertEqual(datas[0].time_id, 1)
    #         self.assertEqual(datas[0].value, 25)
    #         self.assertEqual(datas[0].sensor_id, 1)

    #     with self.subTest('Second'):
    #         self.assertEqual(datas[1].id, 2)
    #         self.assertEqual(datas[1].time_id, 1)
    #         self.assertEqual(datas[1].value, 21)
    #         self.assertEqual(datas[1].sensor_id, 2)

    # def test_relationship_category_sensor(self):
    #     """Test of category-sensor relationship."""
    #     categorys = models.Category.query.all()
    #     with self.subTest('First'):
    #         self.assertEqual(categorys[0].name, 'Температура')
    #         self.assertEqual(categorys[0].sensors[0].name, 'First')

    #     with self.subTest('Second'):
    #         self.assertEqual(categorys[1].name, 'Энергопотребление')
    #         self.assertEqual(categorys[1].sensors[0].name, 'Second')

    #     # for category in categorys:
    #     #     print(category.name)
    #     #     for sensor in category.sensors:
    #     #         print(sensor.id, sensor.name)

    # def test_relationship_sensor_data(self):
    #     """Test of sensor-data relationship."""
    #     sensors = models.Sensor.query.all()
    #     with self.subTest('First'):
    #         self.assertEqual(sensors[0].name, 'First')
    #         self.assertEqual(sensors[0].datas[0].value, 25.0)

    #     with self.subTest('Second'):
    #         self.assertEqual(sensors[1].name, 'Second')
    #         self.assertEqual(sensors[1].datas[0].value, 21.0)

    #     # for sensor in sensors:
    #     #     print(sensor.name)
    #     #     for data in sensor.datas:
    #     #         print(data.id, data.value)

    # def test_relationship_date_time(self):
    #     """Test of date-time relationship."""
    #     date = models.Date.query.first()
    #     self.assertEqual(date.value, self.datetime.date())
    #     self.assertEqual(date.times[0].value, self.datetime.time())

    #     # print(date.value)
    #     # for time in date.times:
    #     #     print(time.id, time.value)

    # def test_relationship_time_data(self):
    #     """Test of date-time relationship."""
    #     time = models.Time.query.first()
    #     self.assertEqual(time.value, self.datetime.time())
    #     self.assertEqual(time.datas[0].value, 25.0)
    #     self.assertEqual(time.datas[1].value, 21.0)

    #     # print(time.value)
    #     # for data in time.datas:
    #     #     print(data.id, data.value)


if __name__ == "__main__":
    unittest.main()
