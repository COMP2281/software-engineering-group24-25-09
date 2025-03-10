import os
import pickle


class Saver:
    def file_exists(self) -> bool:
        """
        Check if data file exists.
        :return: True if file exists, False otherwise.
        """
        return os.path.isfile(self.file_path)

    def load_data(self) -> None:
        """
        Load data from the file if it exists.
        """
        if self.file_exists():
            file = open(self.file_path, "rb")
            self.data = pickle.load(file)

    def __init__(self, data_path: str, file_name: str) -> None:
        """
        Load data.
        :param data_path: Path to data directory.
        """
        self.file_path = os.path.join(data_path, file_name + ".pickle")
        self.data = {}
        self.load_data()

    def save_data(self) -> None:
        """
        Save data to the file.
        A new file is created if none exists.
        """
        file = open(self.file_path, "wb")
        pickle.dump(self.data, file)
