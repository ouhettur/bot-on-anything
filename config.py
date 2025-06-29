# encoding:utf-8

import json
import os

config = {}


def load_config(config_path="./config.json"):
    global config
    if not os.path.exists(config_path):
        print(f"配置文件 {config_path} 不存在，将使用模板 config-template.json")
        config_path = "config-template.json"

    config_str = read_file(config_path)
    # 将json字符串反序列化为dict类型
    config = json.loads(config_str)

    # Override config with environment variables from Railway
    model_type = os.environ.get("LLM_MODEL")
    if model_type:
        config["model"]["type"] = model_type

    api_key = os.environ.get("LLM_API_KEY")
    if api_key:
        if "openai" not in config["model"]:
            config["model"]["openai"] = {}
        config["model"]["openai"]["api_key"] = api_key

    model_name = os.environ.get("LLM_MODEL_NAME")
    if model_name:
        if "openai" not in config["model"]:
            config["model"]["openai"] = {}
        config["model"]["openai"]["model"] = model_name

    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if telegram_bot_token:
        if "telegram" not in config["channel"]:
            config["channel"]["telegram"] = {}
        config["channel"]["telegram"]["bot_token"] = telegram_bot_token

    prompt = os.environ.get("PROMPT")
    if prompt:
        if "openai" not in config["model"]:
            config["model"]["openai"] = {}
        config["model"]["openai"]["character_desc"] = prompt

    print("Load config success")
    return config

def get_root():
    return os.path.dirname(os.path.abspath( __file__ ))


def read_file(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()


def conf():
    return config


def model_conf(model_type):
    return config.get('model').get(model_type)

def model_conf_val(model_type, key):
    val = config.get('model').get(model_type).get(key)
    if not val:
        # common default config
        return config.get('model').get(key)
    return val


def channel_conf(channel_type):
    return config.get('channel').get(channel_type)


def channel_conf_val(channel_type, key, default=None):
    val = config.get('channel').get(channel_type).get(key)
    if not val:
        # common default config
        return config.get('channel').get(key, default)
    return val


def common_conf_val(key, default=None):
    if not config.get('common'):
        return default
    return config.get('common').get(key, default)
