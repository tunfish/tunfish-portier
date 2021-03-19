from pathlib import Path

from sqlalchemy import inspect
import pysodium

from environs import Env


def sa_to_dict(obj):
    """
    Serialize SQLAlchemy object to dictionary.
    - https://stackoverflow.com/a/37350445
    - https://docs.sqlalchemy.org/en/14/core/inspection.html
    :param obj:
    :return:
    """
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def gen_keypair():
    return pysodium.crypto_box_keypair()


def read_config():
    here = Path(__file__).parent.parent.parent

    env = Env(expand_vars=True)
    env.read_env(here / 'etc/tunfish/config/.env', recurse=False)
