import unittest
import os.path
from tempfile import NamedTemporaryFile
from src.server.utils.yaml_datastore import YamlDatastore


class TestYamlDatastore(unittest.TestCase):
    def setUp(self):
        self.yaml_file = NamedTemporaryFile(delete=False)
        self.yaml_file.close()

    def tearDown(self):
        if os.path.exists(self.yaml_file.name):
            os.remove(self.yaml_file.name)

    def test_load_record_when_file_doesnt_exist(self):
        os.remove(self.yaml_file.name)
        datastore = YamlDatastore(self.yaml_file.name)
        self.assertDictEqual(datastore.data, {})

    def test_create_record(self):
        datastore = YamlDatastore(self.yaml_file.name)
        datastore.create_record('key1', 'value1')
        self.assertEqual(datastore.data, {'key1': 'value1'})
        datastore.create_record('key2', 'value2')
        self.assertEqual(datastore.data, {'key1': 'value1', 'key2': 'value2'})
        with self.assertRaises(KeyError):
            datastore.create_record('key1', 'value3')

    def test_read_record(self):
        datastore = YamlDatastore(self.yaml_file.name)
        datastore.create_record('key1', 'value1')
        datastore.create_record('key2', 'value2')
        self.assertEqual(datastore.read_record('key1'), 'value1')
        self.assertEqual(datastore.read_record('key2'), 'value2')
        with self.assertRaises(KeyError):
            datastore.read_record('key3')

    def test_update_record(self):
        datastore = YamlDatastore(self.yaml_file.name)
        datastore.create_record('key1', 'value1')
        datastore.update_record('key1', 'value2')
        self.assertEqual(datastore.read_record('key1'), 'value2')
        with self.assertRaises(KeyError):
            datastore.update_record('key2', 'value2')

    def test_delete_record(self):
        datastore = YamlDatastore(self.yaml_file.name)
        datastore.create_record('key1', 'value1')
        datastore.delete_record('key1')
        self.assertEqual(datastore.data, {})
        with self.assertRaises(KeyError):
            datastore.delete_record('key2')

    def test_get_record_by_id(self):
        datastore = YamlDatastore(self.yaml_file.name)
        datastore.create_record('key1', {'id': 1, 'type': 'test', 'value': 'value1'})
        datastore.create_record('key2', {'id': 2, 'type': 'test', 'value': 'value2'})
        datastore.create_record('key3', {'id': 3, 'type': 'other', 'value': 'value3'})
        record = datastore.get_record_by_id('test', 2)
        self.assertEqual(record, {'id': 2, 'type': 'test', 'value': 'value2'})
        with self.assertRaises(KeyError):
            datastore.get_record_by_id('test', 3)

    def test_get_next_id(self):
        datastore = YamlDatastore(self.yaml_file.name)
        self.assertEqual(datastore.get_next_id(), 1)
        datastore.create_record('key1', {'id': 1, 'type': 'test', 'value': 'value1'})
        self.assertEqual(datastore.get_next_id(), 2)
        datastore.create_record('key2', {'id': 3, 'type': 'test', 'value': 'value2'})
        self.assertEqual(datastore.get_next_id(), 4)
