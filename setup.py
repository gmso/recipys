import setuptools
import re
import ast


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("recipys/__init__.py", "rb") as f:
    _app_name_re = re.compile(r"__app_name__\s+=\s+(.*)")
    app_name = str(
        ast.literal_eval(
            _app_name_re.search(f.read().decode("utf-8")).group(1)
        )
    )

with open("recipys/__init__.py", "rb") as f:
    _version_re = re.compile(r"__version__\s+=\s+(.*)")
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )


setuptools.setup(
    name=app_name,
    version=version,
    author="Germán Mené Santa Olaya",
    author_email="german.mene@gmail.com",
    description=(
        "Get recipes instantly with this CLI tool. "
        "Choose specific meals or ingredients to cater to your appetite!"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/gmso/{app_name}",
    packages=setuptools.find_packages(
        include=[
            f"{app_name}*",
        ]
    ),
    python_requires=">3.8.0",
    install_requires=[
        "beautifulsoup4",
        "requests" "rich",
    ],
    setup_requires=["pytest-runner", "flake8", "black"],
    tests_require=["pytest", "pytest-cov"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    entry_points={"console_scripts": [f"{app_name} = {app_name}.App:main"]},
)
