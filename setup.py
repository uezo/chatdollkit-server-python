from setuptools import setup, find_packages

with open("./chatdollkit/version.py") as f:
    exec(f.read())

setup(
    name="chatdollkit",
    version=__version__,
    url="https://github.com/uezo/chatdollkit-server-python",
    author="uezo",
    author_email="uezo@uezo.net",
    maintainer="uezo",
    maintainer_email="uezo@uezo.net",
    description="SDK to create remote skill server for ChatdollKit.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["examples*", "develop*", "tests*"]),
    install_requires=["pydantic"],
    license="Apache v2",
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
