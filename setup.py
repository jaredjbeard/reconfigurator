from setuptools import setup

import os

os.chmod('reconfigurator/scripts/add_cli.sh', 0o755) #rwxr-xr-x

setup(
    name="reconfigurator",
    version="0.0.1",
    install_requires=[],
    scripts=['reconfigurator/scripts/add_cli.sh'],
    data_files=[('scripts', ['reconfigurator/scripts/add_cli.sh'])],
)
