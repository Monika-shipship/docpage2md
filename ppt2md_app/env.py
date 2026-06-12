import os


def get_dashscope_api_key():
    return get_env_value("DASHSCOPE_API_KEY")


def get_deepseek_api_key():
    return get_env_value("DEEPSEEK_API_KEY")


def get_env_value(name):
    if os.name == "nt":
        user_key = _get_windows_user_env(name)
        if user_key:
            return user_key

    return os.getenv(name)


def _get_windows_user_env(name):
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as env_key:
            value, _ = winreg.QueryValueEx(env_key, name)
            return value or None
    except OSError:
        return None
