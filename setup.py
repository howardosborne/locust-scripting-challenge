from setuptools import find_packages, setup

setup(
    name='locust-scripting-challenge',
    version='0.1.0',
    packages=['locust-script-challenge'],
    description='A challenge to help learn how to write a performance test script',
    url='https://github.com/howardosborne/locust-scripting-challenge',
    author='Howard Osborne',
    author_email='howardosborneconsulting@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'lxml'
    ],
)