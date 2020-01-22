from setuptools import setup
import sys

setup(
    name='Prozedurale-Vegetationsverteilung',
    version='1.0',
    description='TODO',
    author='Martin Lesser',
    author_email='martin.lesser@mailbox.org',
    packages=['intern'],
    install_requires=[
        "Babel >= 2.7.0",
        "psutil >= 5.6.3",
        "pytz >= 2019.1",
        "tkfilebrowser >= 2.3.1",
        "Image >= 1.5.27",
        "imageio >= 2.5.0",
        "matplotlib >= 3.1.1",
        "pyyaml"
    ] + [] if "win" in sys.platform else [] #"pywin32 >= 224"
      + [] if "darwin" in sys.platform else [],
)
