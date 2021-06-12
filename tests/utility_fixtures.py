from pathlib import Path
from pytest import fixture
from recipys.ConfigFile import ConfigFile


@fixture
def config_file_cleanup():
    file_path = Path(ConfigFile().file_name)
    file_path.unlink(missing_ok=True)  # delete config file if exists
    yield
    file_path.unlink()  # delete config file
