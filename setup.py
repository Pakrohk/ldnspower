# setup.py
from setuptools import setup, find_packages

setup(
    name="dns_changer",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "typer==0.9.0",
        "rich==13.7.0",
        "dnspython==2.6.0",
        "polycli==0.1.3",
    ],
    entry_points={
        "console_scripts": [
            "dns-changer=dns_changer.cli:app",
        ],
    },
    author="Pakrohk",
    author_email="pakrohk@gamil.com",
    description="An enhanced DNS changer tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

