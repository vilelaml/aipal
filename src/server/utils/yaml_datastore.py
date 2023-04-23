import yaml
import os.path
from typing import Dict


class YamlDatastore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.file_path, 'w') as f:
            yaml.dump(self.data, f)

    def create_record(self, key, value):
        if key in self.data:
            raise KeyError(f"Record with key '{key}' already exists")
        self.data[key] = value
        self.save_data()

    def read_record(self, key):
        try:
            return self.data[key]
        except KeyError:
            raise KeyError(f"Record with key '{key}' does not exist")

    def update_record(self, key, value):
        if key not in self.data:
            raise KeyError(f"Record with key '{key}' does not exist")
        self.data[key] = value
        self.save_data()

    def delete_record(self, key):
        try:
            del self.data[key]
            self.save_data()
        except KeyError:
            raise KeyError(f"Record with key '{key}' does not exist")

    def get_record_by_id(self, record_type: str, record_id: int) -> Dict:
        for record in self.data.values():
            if record.get("id") == record_id and record.get("type") == record_type:
                return record
        raise KeyError(f"No {record_type} record found with id {record_id}")

    def get_next_id(self) -> int:
        max_id = 0
        for record in self.data.values():
            if record.get("id", 0) > max_id:
                max_id = record["id"]
        return max_id + 1 if max_id else 1
