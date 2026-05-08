from setuptools import setup, find_packages

setup(
    name="settingslib",
    version="0.1.0",
    description="A library to manage settings files in TOML and JSON.",
    author="Nicolás Miranda Colivoro",
    author_email="nmcolivoro@outlook.cl",
    install_requires=[
        "tomlkit==0.13.3",
        "typing_extensions==4.15.0"
    ],
    packages=find_packages()
)