from setuptools import setup, find_packages

setup(
    name='hello_world_flask',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'hello-world=run:main'
        ]
    },
)
