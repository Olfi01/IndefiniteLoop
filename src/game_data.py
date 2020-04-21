"""A helper class to handle saved game data on the device. Uses JSON encoding to read and write data."""
import json
import os.path


class GameData:
    """The class that handles data reading/writing."""
    def __init__(self, save_file_path):
        """Initializes a new instance of the GameData class. Takes the path of the save file as an argument.
        If the save file does not exist, a new one will be created.
        :type save_file_path: str"""
        self.file_path = save_file_path
        try:
            with open(self.file_path) as json_file:
                self.data = json.load(json_file)
        except IOError:
            self.data = {}

    def save(self):
        """Saves the current data to the JSON file"""
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)

    def get_max_level(self):
        """Returns the maximum unlocked level number"""
        return self.get_or_default("max_level", 1)

    def get_or_default(self, key, default_value):
        """Generic method to either return a value if it's already present
        or set it to a default value before returning that."""
        if key not in self.data:
            self.data[key] = default_value
        self.save()
        return self.data[key]
