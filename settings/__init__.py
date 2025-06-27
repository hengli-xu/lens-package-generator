import os
import yaml
from enum import Enum

# env_key = key_to_env(os.environ['environment'])
# locale_key = key_to_env(os.environ['locale'])
# platform_key = os.environ['platform']
env_key = "SIT"
locale_key = "CA"


def read_yaml_file(current_path):
    print("current directory -> %s" % os.getcwd())
    yml_file = os.path.abspath(current_path + "/fa_config.yaml")
    yml = open(yml_file, 'r', encoding='utf-8')
    if os.path.isfile(yml_file):
        return yml.read()
    else:
        print(yml_file + 'file not exist')


current_path = os.path.dirname(__file__)
global yaml_cfg
yaml_cfg = yaml.full_load(read_yaml_file(current_path))


if not yaml_cfg:
    raise Exception("Failed to load YAML configuration.")

def get_current_env(specific_env):
    env = ''
    try:
        env = yaml_cfg.get(specific_env)[str.upper(env_key)]
    except Exception as e:
        print("{0} do not define in {1} env, just skip it, please double check if it's necessary".format(specific_env,
                                                                                                         env_key))
    finally:
        return env


class Locale:
    US = "US"
    CA = "CA"



def key_to_env(key):
    envs = {
        "QA": "QA",
        "UAT": "UAT",
        "STG": "STG",
        "Prod": "Prod",
    }
    return envs.get(key, None)

