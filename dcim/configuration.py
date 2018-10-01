from yaml import load
from collections import defaultdict


# accepts a key string, searches conf.yaml for key, binds to default dictionary and returns it
def get_config(key):
    try:
        conf = load(open("conf.yaml"))[key]
    except KeyError as err:
        print("Key error: {0}".format(err))

    else:
        conf_data = defaultdict(list)

        for item in conf:
            conf_data[item] = conf[item]

        return conf_data
