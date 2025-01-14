import sys


def pytest_configure():
    root_dir: str = "/home/ghaz/flask_gateway/"
    sys.path.append(root_dir)

    from generate_env import (  # pylint: disable=import-error, import-outside-toplevel
        load_environment,
    )

    load_environment()
