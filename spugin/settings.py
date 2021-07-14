import appdirs
from pathlib import Path

# Static values
VERSION = 0.1
API_URL = "http://api.spiget.org/v2"
USER_AGENT = f"Spugin/{VERSION}"
CONFIG_FILE = Path(f"{appdirs.user_config_dir(appname='spugin')}/spugin.yml").__str__()
