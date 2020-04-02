import json


class Store():
    def __init__(self, file_name):
        self._file = file_name
        if not self._read_file(): # If the file doesn't exist, or is empty, write an empty object to it
            self.write(None, {})

    def _read_file(self):
        try:
            with open(self._file, 'r') as f:
                return json.loads(f.read())
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return None

    def read(self, key=None):
        data = self._read_file() # Always reread file since it might be edited externally
        if key is not None:
            return self._read_file().get(key)
        return data

    def write(self, key, value):
        data = self._read_file()
        if key is None:
            data = value
        else:
            data[key] = value
        with open(self._file, 'w') as json_file:
            json_file.write(json.dumps(data))

    def __setitem__(self, key, value): # Intrinsic dict methods called when writing or accessing dicts
        self.write(key, value)

    def __getitem__(self, key):
        return self.read(key)