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
        self.file_name: str = "config.json"
        self.user_agent: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) "
            "Gecko/20100101 Firefox/89.0"
        )
        self.headers: Dict[str, str] = {
            "User-Agent": self.user_agent,
            "Accept": (
                "text/html,application/xhtml+xml,application/xml"
                ";q=0.9,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.duckduckgo.com/",
        }
        self.last_request: float = time.time()

    def get_delta_last_request(self) -> float:
        """
        Time difference between now and last request (saved in config file)

        Returns:
            - float: Seconds between current time and last request
        """
        self._read_config_file()
        return time.time() - self.last_request

    def update_time_last_request(self) -> None:
        """
        Update timestamp of last request, both locally and in config file
        """
        self._create_config_file()

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

        Raises:
            - OSError: if KeyError Exception ocurrs (accessing dict)
        """
        data: Dict[str, str] = json.load(file)
        try:
            self.headers = self._get_headers_from_json_file(data)
            self.user_agent = self.headers["User-Agent"]
            self.last_request = self._get_last_request_from_json_file(data)
        except KeyError:
            raise OSError

    def _create_config_file(self) -> None:
        """
        Create the config file anew using default values
        """
        new_config_file = ConfigFile()
        self.headers = new_config_file.headers
        self.last_request = new_config_file.last_request
        dict_for_json_file: Dict[str, str] = {
            "headers": str(self.headers),
            "last_request": str(self.last_request),
        }
        with open(self.file_name, "w") as file:
            json.dump(dict_for_json_file, file)

    def _get_headers_from_json_file(
        self, data: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Return headers dictionary from json loaded data

        Args:
            - data: dictionary of loaded json data

        Raises:
            - KeyError: if json file is tampered
                (instance keys and dictionary are different)
        """
        headers: str = data["headers"].replace("'", '"')
        json_headers: Dict[str, str] = json.loads(headers)
        if json_headers.keys() != self.headers.keys():
            raise KeyError  # tampered json file -> reset it
        return json_headers

    def _get_last_request_from_json_file(self, data: Dict[str, str]) -> str:
        """
        Return last_request dictionary value from json loaded data

        Args:
            - data: dictionary of loaded json data

        Raises:
            - KeyError: if json file is tampered
                (instance keys and dictionary are different)
        """
        try:
            json_num = float(data.get("last_request"))
            own_num = float(self.last_request)
            if json_num == 0 or own_num < json_num:
                raise ValueError
            return json_num
        except ValueError:
            raise KeyError
