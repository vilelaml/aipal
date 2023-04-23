import os
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.server.agent.agent import Agent
from src.server.utils.yaml_datastore import YamlDatastore
from src.server.utils.yaml_record import YamlRecord


class TestYamlRecord(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.ds_patcher = patch.object(YamlRecord, 'BASE_PATH', self.temp_dir.name)
        self.ds_patcher.start()
        self.file_name = f'{self.temp_dir.name}/YamlRecord.yaml'

        self.record1 = YamlRecord()
        self.record2 = YamlRecord()

    def tearDown(self):
        self.ds_patcher.stop()
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            os.rmdir(self.temp_dir.name)

    def test_save(self):
        self.record1.save()
        self.record2.save()
        datastore = YamlDatastore(self.file_name)
        self.assertEqual(len(datastore.data), 2)

    def test_get(self):
        self.record1.save()
        self.record2.save()
        record = YamlRecord.get(2)
        self.assertEqual(record.id, 2)

    def test_update(self):
        class YamlWithAttr(YamlRecord):
            def __init__(self, id = None, new_attr = None):
                super().__init__(id)
                self.new_attr = new_attr

        record1 = YamlWithAttr(new_attr="test")
        record1.save()
        record1.new_attr = "updated!"
        record1.update()
        record = YamlWithAttr.get(1)
        self.assertEqual(record.new_attr, "updated!")

    def test_delete(self):
        self.record1.save()
        self.record2.save()
        self.record2.delete()
        datastore = YamlDatastore(self.file_name)
        self.assertEqual(len(datastore.data), 1)
        with self.assertRaises(KeyError):
            Agent.get(2)

    def test___attr__(self):
        self.record1.save()
        self.assertDictEqual({"type": "YamlRecord", "id": 1}, self.record1.__attr__)
