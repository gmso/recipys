import time
import json
from io import TextIOWrapper
from typing import Dict


class ConfigFile:
    """
    Handles reading and writing of .json config file
    """

    def __init__(self) -> None:
        """
        Initialize instance variables
        """
        self.file_name: str = "config/config.json"
        self.user_agent: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) "
            "Gecko/20100101 Firefox/89.0")
        self.headers: Dict[str, str] = {
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.duckduckgo.com/"
                }
        self.last_request: float = time.time()
    
    def _read_config_file(self) -> None:
        """
        Read config file and update instance variables
        """
        try:
            with open(self.file_name, "r") as file:
                self._update_from_file(file)
        except OSError:
            self._create_config_file()

    def _update_from_file(self, file: TextIOWrapper) -> None:
        """
        Update instance variables from file

        Args:
            - file: file handle of json file
        """
        data = json.load(file)

        try:
            self.headers = dict(data["headers"])
            self.user_agent = self.headers["User-Agent"]
            self.last_request = float(data["last_request"])
        except KeyError:
            raise OSError
    
    def _create_config_file(self) -> None:
        """
        Create the config file anew using instance variables
        """
        dict_for_json_file: Dict[str, str] = {
            "headers": str(self.headers),
            "last_request": str(self.last_request)
        }
        with open(self.file_name, "r") as file:
            json.dump(dict_for_json_file, file)
