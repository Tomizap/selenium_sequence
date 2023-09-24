from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = "0.0.1"
DESCRIPTION = """
Simple Python Package
"""

setup(
    name="selenium_sequence",
    version=VERSION,
    author="TZ",
    author_email="zaptom.pro@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "flask",
        "colorama",
        "requests",
        # "indeed @ git+https://github.com/Tomizap/indeed.git#egg=indeed",
        # "linkedin @ git+https://github.com/Tomizap/linkedin.git#egg=linkedin"
        "tzmongo @ git+https://github.com/Tomizap/tzmongo.git#egg=tzmongo",
        "selenium_driver @ git+https://github.com/Tomizap/selenium_driver.git#egg=selenium_driver"],
    keywords=[],
    classifiers=[]
)