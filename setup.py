from setuptools import setup

import os

os.chmod('reconfigurator/scripts/post_install.sh', 0o755) #rwxr-xr-x

setup(
    name="reconfigurator",
    version="0.0.1",
    install_requires=[],
    scripts=['reconfigurator/scripts/post_install.sh'],
    data_files=[('scripts', ['reconfigurator/scripts/post_install.sh'])],
)
