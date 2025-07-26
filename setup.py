from setuptools import setup, find_packages

setup(
    name="buyursin-bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aiogram==3.16.0",
        "aiohttp==3.11.11", 
        "aiosqlite==0.21.0",
        "requests==2.32.3",
        "python-dotenv==1.0.1",
    ],
    python_requires=">=3.8",
) 