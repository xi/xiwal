from setuptools import find_packages
from setuptools import setup


setup(
    name='wal',
    version='0.0.0',
    description='Generate terminal color schemes',
    author='Tobias Bengfort',
    author_email='tobias.bengfort@posteo.de',
    packages=find_packages(),
    entry_points={'console_scripts': [
        'wal=wal.__main__:main',
    ]},
    license='MIT',
)
