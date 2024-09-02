from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="octopush",
    version="1.0",
    description="Play with Octopus energy API",
    py_modules=["octopush"],
    entry_points={
        "console_scripts": [
            "octopush=octopush:main",
        ],
    },
    install_requires=required
)
