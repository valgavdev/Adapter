import sys

from config import config

if config.common_lib:
    sys.path.append(config.common_lib)

from adapter import maker

app_sets = maker.create_settings()
