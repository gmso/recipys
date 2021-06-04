import time
from recipys.ConfigFile import ConfigFile


def test_ConfigFile_construction():
    config_file = ConfigFile()
    assert config_file.file_name == "config/config.json"
    assert config_file.user_agent == (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) "
            "Gecko/20100101 Firefox/89.0")
    assert config_file.headers == {
                "User-Agent": config_file.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.duckduckgo.com/"
            }
    assert (config_file.last_request - time.time() < 1)