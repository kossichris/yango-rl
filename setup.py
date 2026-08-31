from setuptools import setup

setup(
    name="yango-rl",
    version="1.0.0",
    description="Driver Repositioning Optimization using Reinforcement Learning",
    author="Christian Kossi Placktor Hounsounou",
    author_email="chrishouns21@gmail.com",
    packages=["env", "agents", "train", "utils"],
    package_data={
        "": ["*.py"],
    },
    python_requires=">=3.9",
)
