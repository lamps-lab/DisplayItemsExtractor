import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="table_and_fig_ref_extraction",
    version="0.0.1",
    author="Yasasi Abeysinghe",
    description="This code repository contains libraries and applications of Python programs that extract figures and tables references from the text in scientific papers.",
    url="https://github.com/lamps-lab/TableAndFigureReferenceExtractor",
    project_urls={
        "Bug Tracker": "https://github.com/lamps-lab/TableAndFigureReferenceExtractor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
