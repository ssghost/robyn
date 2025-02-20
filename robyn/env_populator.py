from distutils.command.config import config
import os
import logging
from pathlib import Path


# set the logger that will log the environment variables imported from robyn.env and the ones already set
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# parse the configuration file returning a list of tuples (key, value) containing the environment variables
def parser(config_path=None, project_root=""):
    """Find robyn.env file in root of the project and parse it"""
    if config_path is None:
        config_path = Path(project_root) / "robyn.env"

    if config_path.exists():
        with open(config_path, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                yield line.strip().split("=")


# check for the environment variables set in cli and if not set them
def load_vars(variables=None, project_root=""):
    """Main function"""

    if variables is None:
        variables = parser(project_root=project_root)

    for var in variables:
        if var[0] in os.environ:
            logger.info(f" Variable {var[0]} already set")
            continue
        else:
            os.environ[var[0]] = var[1]
            logger.info(f" Variable {var[0]} set to {var[1]}")
