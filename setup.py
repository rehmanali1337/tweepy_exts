import setuptools
from typing import List

required_packages: List[str] = []


setuptools.setup(
    name="tweepy_exts",
    version="0.1.0",
    author="Rehman Ali",
    author_email="rehmanali.9442289@gmail.com",
    description="A wrapper for official tweepy for more simple usage",
    url="https://github.com/rehmanali1337/tweepy_exts",
    packages=setuptools.find_packages(),
    install_requires=required_packages
)
