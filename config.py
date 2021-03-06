from configparser import ConfigParser


def config(filename, section):
    # create a parser
    config = ConfigParser()
    # read config file
    config.read(filename)

    # get section
    db = {}
    if config.has_section(section):
        params = config.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db