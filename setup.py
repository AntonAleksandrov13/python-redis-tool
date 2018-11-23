import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redis-tools",
    version="1.2.1",
    author="AntonAleksandrov",
    author_email="antonaleksandrov24@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntonAleksandrov13/python-redis-tool.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['redis-tool=cmd.__main__:main'],
    }
)
