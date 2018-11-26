import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redis-cluster-tool",
    version="1",
    author="Anton Aleksandrov",
    author_email="antonaleksandrov24@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntonAleksandrov13/python-redis-tool.git",
    packages=['cli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['redis-cluster-tool=cli.__main__:main'],
    }
)
