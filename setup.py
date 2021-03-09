from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="SimpTextAlignPython",
    version="0.0.1",
    author=".",
    author_email=".",
    description="Desc",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="....",
    packages=find_packages(),
    install_requires=[
        "nltk==3.4.5",
        "numpy==1.17.2",
        "textblob==0.15.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
