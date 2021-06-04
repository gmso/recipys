import time
from pathlib import Path
from recipys.ConfigFile import ConfigFile


def test_ConfigFile_construction():
    config_file = ConfigFile()
    assert config_file.file_name == "config.json"
    assert config_file.user_agent == (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) "
            "Gecko/20100101 Firefox/89.0")
    assert config_file.headers == {
                "User-Agent": config_file.user_agent,
                "Accept": (
                    "text/html,application/xhtml+xml,application/xml"
                    ";q=0.9,image/webp,*/*;q=0.8"),
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.duckduckgo.com/"
            }
    assert (config_file.last_request - time.time() < 1)


def test_read_config_file():
    config_file = ConfigFile()
    file_path = Path(config_file.file_name)
    file_path.unlink(missing_ok=True)  # delete config file if exists
    assert not Path(config_file.file_name).is_file()

    # File does not exist -> created with default values
    config_file._read_config_file()
    assert Path(config_file.file_name).is_file()

    config_file.user_agent = "test_user_agent"
    config_file.headers["User-Agent"] = config_file.user_agent
    config_file.last_request = 999

    # File exists -> instance variables overwritten with file content
    config_file._read_config_file()
    assert Path(config_file.file_name).is_file()
    assert config_file.user_agent != "test_user_agent"
    assert config_file.headers["User-Agent"] != "test_user_agent"
    assert config_file.last_request != 999

    file_path.unlink()  # delete config file
