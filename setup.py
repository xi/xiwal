from setuptools import find_packages
from setuptools import setup


setup(
    name='xiwal',
    version='0.0.0',
    description='Generate terminal color schemes',
    url='https://github.com/xi/xiwal',
    author='Tobias Bengfort',
    author_email='tobias.bengfort@posteo.de',
    packages=find_packages(),
    entry_points={'console_scripts': [
        'xiwal=xiwal.__main__:main',
    ]},
    license='MIT',
)
