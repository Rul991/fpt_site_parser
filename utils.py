import json
import work_with_files as fw

def get_config(prop = ''):
    config: dict = json.load(open('json/config.json'))
    if len(prop):
        if prop in config.keys():
            return config[prop]

    return config

def info(m, bot, text):
    print(text)
    bot.send_message(m.chat.id, text)

def edit_config(new_config_value: dict):
    config = get_config()
    for key, value in new_config_value.items():
        if type(config[key]) is list:
            config[key].append(value)
        else:
            config[key] = value

    fw.file_writer('json/config.json', json.dumps(config, indent=3))

