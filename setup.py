from setuptools import find_packages, setup

setup(
    name='locust_scripting_challenge',
    version='0.1.0',
    packages=['locust_script_challenge'],
    description='A challenge to help learn how to write a performance test script',
    url='https://github.com/howardosborne/locust_scripting_challenge',
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