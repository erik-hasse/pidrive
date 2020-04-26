import setuptools

setuptools.setup(
    name='pidrive',
    version='0.1',
    author='Erik Hasse',
    author_email='erik.g.hasse@gmail.com',
    description='Control a small car with a Raspberry Pi',
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'smbus2',
    ]
)
