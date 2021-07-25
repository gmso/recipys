from pathlib import Path
from pytest import fixture
from recipys.ConfigFile import ConfigFile


@fixture
def config_file_cleanup():
    file_path = Path(ConfigFile().file_name)
    try:
        file_path.unlink()  # delete config file if exists
    except FileNotFoundError:
        pass

    yield

    try:
        file_path.unlink()  # delete config file
    except FileNotFoundError:
        pass
