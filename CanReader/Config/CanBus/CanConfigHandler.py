import logging

from CanReader.Config.CanBus.CanDataConfig import CanDataConfig
from CanReader.Config.ConfigHandler import ConfigHandler


class CanConfigHandler(ConfigHandler):
    """
        :Inherit: :class:`ConfigHandler`

        :Description:
            Main task is to handle CAN config file.\n
            Can load config and return it as a list of CanDataConfig objects,
            or update config sections from given CanDataConfig object.

        :param config_file_name: Name of config file.
        :type config_file_name: str

        :raises:
            For error handling see base class :class:`ConfigHandler`.

    """

    def __init__(self, config_file_name="can_config.ini"):
        ConfigHandler.__init__(self, config_file_name=config_file_name)

    def update_section_in_config(self, data_config):
        """
            :Description:
                Update config section with new config for already existing section.\n
                Automatically save changes to file.

            :param data_config: Updated section config
            :type data_config: CanDataConfig

            :raises TypeError:
                Parameter data_config is not a CanDataConfig type.

        """
        self.check_update_parameter_type(data_config)

        section_id = str(data_config.id)

        if data_config.unit == "%":
            unit = "%%"
        else:
            unit = data_config.unit

        self.config.set(section_id, "Group id", str(data_config.group_id))
        self.config.set(section_id, "Widget id", str(data_config.widget_id))
        self.config.set(section_id, "Overview id", str(data_config.overview_id))
        self.config.set(section_id, "Name", data_config.name)
        self.config.set(section_id, "Unit", unit)
        self.config.set(section_id, "Can id", str(data_config.can_id))
        self.config.set(section_id, "Start bit", str(data_config.start_bit))
        self.config.set(section_id, "Length", str(data_config.length))
        self.config.set(section_id, "Multiplier", str(data_config.multiplier))
        self.config.set(section_id, "Offset", str(data_config.offset))
        self.config.set(section_id, "Endian", str(data_config.endian))

        self.save_config()

    def load_from_config_file(self):
        """
            :Description:
                Load every section saved in config file to list of DataConfig objects.

            :return: List of DataConfig object.
            :rtype: list[CanDataConfig]
        """
        data_config_list = []
        sections = self.config.sections()

        for section in sections:
            data_config = self.load_selected_from_config_file(int(section))
            data_config_list.append(data_config)

        return data_config_list

    def load_selected_from_config_file(self, config_id):
        """
            :Description:
                Load selected section from config file.\n
                Section is selected by unique id.

            :param config_id: Id of data config section.
            :type config_id: int

            :return: data in form of object DataConfig for selected configuration
            :rtype: CanDataConfig

            :raises TypeError:
                Config id is not an integer.

            :raises ValueError:
                Config id is not in range of existing config sections.
        """

        self.check_config_id(config_id)

        section = str(config_id)
        widget_id = self.config.getint(section, "Widget id")
        group_id = self.config.getint(section, "Group id")
        overview_id = self.config.getint(section, "Overview id")
        name = self.config.get(section, "Name")
        unit = self.config.get(section, "Unit")
        can_id = self.config.get(section, "Can id")
        start_bit = self.config.getint(section, "Start bit")
        length = self.config.getint(section, "Length")
        multiplier = self.config.getfloat(section, "Multiplier")
        offset = self.config.getfloat(section, "Offset")
        endian = self.config.get(section, "Endian")

        return CanDataConfig(config_id, group_id, widget_id, overview_id, name, unit,
                             can_id, start_bit, length, multiplier, offset, endian)

    @staticmethod
    def check_update_parameter_type(data_config):
        """
            :Description:
                Check type of data config

            :raises TypeError:
                Parameter data_config is not a CanDataConfig type.
        """
        try:
            if type(data_config) != CanDataConfig:
                raise TypeError
        except TypeError:
            error_msg = "As a parameter is expected CanDataConfig not " + type(data_config)
            logging.exception(error_msg)
            raise TypeError(error_msg)

    @staticmethod
    def check_config_id(config_id):
        """
            :Description:
                Check type and value of config id that is supposed to be loaded

            :raises TypeError:
                Config id is not an integer.

            :raises ValueError:
                Config id is not in range of existing config sections.
        """
        try:
            if type(config_id) != int:
                raise TypeError
            if config_id < 0 or config_id > CanConfigHandler().number_of_data_configs:
                raise ValueError
        except TypeError:
            error_msg = "Config id must be integer"
            logging.exception(error_msg)
            raise TypeError(error_msg)
        except ValueError:
            error_msg = "Config id must be in range of data config in config file 0 - {}" \
                .format(CanConfigHandler().number_of_data_configs)
            logging.exception(error_msg)
            raise ValueError(error_msg)


if __name__ == "__main__":
    config = CanConfigHandler("../can_config.ini")
    data_config_list = config.load_from_config_file()
    print(data_config_list)
