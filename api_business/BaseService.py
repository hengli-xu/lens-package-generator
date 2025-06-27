from settings import env_key, yaml_cfg


class BaseService:
    def __init__(self,  host="", headers={}, token=None):
        current_service = self.__class__.__name__ if "" == host else host
        host_from_config = self.get_current_env(current_service)
        self.host = host if "" == host_from_config else host_from_config
        self.id_token = None

    def get_current_env(self, specific_env):
        env = ''
        try:
            env = yaml_cfg.get(specific_env)[str.upper(env_key)]
        except Exception as e:
            print(
                "{0} do not define in {1} env, just skip it, please double check if it's necessary".format(specific_env,
                                                                                                           env_key))
        finally:
            return env

