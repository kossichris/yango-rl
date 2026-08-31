from setuptools import setup, find_packages

setup(
    name="yango-rl",
    version="1.0.0",
    description="Driver Repositioning Optimization using Reinforcement Learning",
    author="Christian Kossi Placktor Hounsounou",
    author_email="chrishouns21@gmail.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "gymnasium>=0.28.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "torch>=2.0.0",
        "stable-baselines3>=2.0.0",
        "streamlit>=1.28.0",
        "tensorboard>=2.13.0",
        "pillow>=10.0.0",
        "scipy>=1.11.0",
    ],
)
