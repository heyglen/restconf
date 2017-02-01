
import configparser


class ConfigurationFile(object):

    @staticmethod
    def _parse(file_name):
        config = configparser.ConfigParser()
        config.read(file_name)
        settings = dict()
        for section in config.sections():
            for option in config.options(section):
                if section not in settings:
                    settings[section] = dict()
                settings[section][option] = config.get(section, option)
        return settings

    @staticmethod
    def get(file_name):
        return ConfigurationFile._parse(file_name)
