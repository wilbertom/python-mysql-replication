import json
import pathlib



class PositionFile:

    def __init__(self, filename):
        self._filename = filename

        self._binary_log_file = None
        self._binary_log_position = None

        self._binary_log_file, self._binary_log_position = self._load_database()

    @property
    def binary_log_position(self):
        return self._binary_log_position

    @binary_log_position.setter
    def binary_log_position(self, binary_log_position):
        self._binary_log_position = binary_log_position
        self._save()

    @property
    def binary_log_file(self):
        return self._binary_log_file

    @binary_log_file.setter
    def binary_log_file(self, new_binary_log_file):
        self._binary_log_file = new_binary_log_file
        self._save()

    @property
    def _data_file_path(self):
        return pathlib.Path(self._filename)

    def _load_database(self):
        self._create_initial_data_file()
        data = json.load(open(self._data_file_path, "r"))
        return data["binary_log_file"], data["binary_log_position"]

    def _create_initial_data_file(self):
        if not self._data_file_path.exists():
            self._data_file_path.parent.mkdir(exist_ok=True)
            self._data_file_path.touch()
            self._save()

    def _save(self):
        self._data_file_path.write_text(json.dumps(
            {
                "binary_log_file": self.binary_log_file,
                "binary_log_position": self.binary_log_position,
            },
            indent=2,
        ))
