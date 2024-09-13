import os
import platform
from lbi_dashboard_autism.const import USERNAME, CONFIG

ENV = CONFIG.get("ENVIRONMENT")


def _get_os() -> str:
    return platform.system()


def _return_dict_from_os(platform: str) -> dict:
    CACHE_DIR_DICT_LINUX = {"dev": "/tmp", "prod": f"/home/{USERNAME}"}

    CACHE_DIR_DICT_WIN = {
        "dev": os.getcwd(),
        "prod": f"C:/Users/{USERNAME}/AppData/Local/Temp",
    }

    CACHE_DIR_BY_OS = {"Linux": CACHE_DIR_DICT_LINUX, "Windows": CACHE_DIR_DICT_WIN}

    return CACHE_DIR_BY_OS.get(platform, CACHE_DIR_DICT_LINUX)


def get_cache_dir():
    _os = _get_os()
    _cache_dict = _return_dict_from_os(_os)
    return _cache_dict.get(ENV)
