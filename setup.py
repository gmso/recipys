import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recipys",
    version="0.0.1",
    author="Germán Mené Santa Olaya",
    author_email="german.mene@gmail.com",
    description="Get recipes instantly with this CLI tool. Choose specific meals or ingredients to cater to your appetite!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gmso/recipys",
    packages = setuptools.find_packages(include = ['recipys*',]),
    install_requires=[
        'rich',
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest','pytest-cov'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    entry_points={
        "console_scripts": [
            "recipys = recipys.App:main"
        ]
    },

)