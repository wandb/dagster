import os


def config_path(path, from_=""):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), from_, "dagster_wandb/launch/compute_config", path
    )


def config_open(path, mode="r"):
    """Returns an opened fixture file"""
    return open(config_path(path), mode)


