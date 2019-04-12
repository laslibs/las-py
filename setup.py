import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="las_py",
    version="1.1.0",
    author="Ikechukwu Eze",
    author_email="iykekings36@gmail.com",
    description="A zero-dependency python library for reading/parsing canadian well-log files (.Las files)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='well log well-log geophysical geophysics las .las',
    url="https://github.com/iykekings/las_py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Documentation': 'https://github.com/iykekings/las_py',
        'Funding': 'https://www.patreon.com/bePatron?u=19152008',
        'Source': 'https://github.com/iykekings/las_py',
        'Tracker': 'https://github.com/iykekings/las_py/issues',
    },
    python_requires='>=3',
)
