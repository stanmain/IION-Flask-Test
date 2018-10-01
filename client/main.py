# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Module of <...>."""

from datetime import datetime
import time
import asyncio
import aiohttp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, contains_eager

from . import models


class Client:
    """Client applocation."""

    def __init__(self, config):
        """Init client."""
        self.config = config
        self.init_db()

    def init_db(self):
        """Init the database."""
        self.engine = create_engine(
            self.config.SQLALCHEMY_DATABASE_URI,
            echo=self.config.SQLALCHEMY_ECHO
        )
        self.session = sessionmaker(bind=self.engine)()

    def run(self):
        """Run client."""
        asyncio.run(self.loop())

    async def loop(self):
        """Make a loop of asynchronous requests."""
        # Waiting for rounded time.
        await asyncio.sleep(60 - int(time.time()) % 60)

        while True:
            start_time = time.time()
            date = datetime.now()
            print(date)
            nodes = self.get_nodes()
            data = await self.get_data(nodes)
            self.push_data(date, data)
            stop_time = time.time()
            await asyncio.sleep(
                self.config.CLIENT_PERIOD - (stop_time - start_time))

    def get_nodes(self):
        """Get nodes from db."""
        query = self.session.query(models.Node.ref)
        query = query.filter(models.Node.enabled == True)
        records = query.all()
        return records

    async def get_data(self, nodes):
        """Get data from nodes."""
        data_dict = []
        futures = [self.fetch(node.ref, node.id) for node in nodes]
        for future in asyncio.as_completed(futures, timeout=10):
            try:
                node_id, temp = await future
                lines = temp.split('\n')
                for line in lines:
                    try:
                        code, value = line.split(' ')
                        data_dict[code] = {
                            'value': value,
                            'node': node_id
                        }
                    except ValueError:
                        pass
            except (asyncio.TimeoutError, aiohttp.ClientError) as e:
                print(e)
        return data_dict

    async def fetch(self, url, node_id):
        """Fetch data from url."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return node_id, await response.text()

    def push_data(self, date, data):
        """Push data into db."""
        current_date = models.DatePoint(id=date.date())
        self.session.merge(current_date)

        current_time = models.TimePoint(id=date, date_id=current_date.id)
        self.session.add(current_time)

        query = self.session.query(models.Category)
        query = query.join(models.Sensor)
        query = query.options(contains_eager(models.Category.sensors))
        categorys = query.all()

        # For registered sensors:
        for category in categorys:
            for sensor in category.sensors:
                try:
                    item = data.pop(sensor.code)
                    data_item = models.Data(
                        value=item['value'],
                        sensor_id=sensor.id,
                        time_id=current_time.id
                    )
                    self.session.add(data_item)
                    sensor.time_id = current_time.id
                    category.time_id = current_time.id
                    node = models.Node(
                        id=item['node'], time_id=current_time.id)
                    self.session.merge(node)
                except KeyError:
                    print(sensor.code, 'not found')
        self.session.commit()

        # For unregistered sensors:
        for code, item in data.items():
            print(code)
            sens = models.Sensor(
                code=code,
                name=code,
                description='',
                node_id=item['node'],
                time_id=current_time.id
            )
            self.session.add(sens)
            node = models.Node(id=item['node'], time_id=current_time.id)
            self.session.merge(node)
            self.session.commit()
            data_item = models.Data(
                value=item['value'],
                sensor_id=sens.id,
                time_id=current_time.id
            )
            self.session.add(data_item)
        self.session.commit()
