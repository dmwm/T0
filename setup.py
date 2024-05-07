from setuptools import setup, find_packages

# Read requirements from requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="T0",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="This package contains the code that is involved in the Tier 0 agent when its deployed",
    author="Dirk Hufnagel",
    author_email="Dirk.Hufnagel@cern.ch",
    maintainer="WMCore",
    maintainer_email="ms.unmerged@cern.ch",
    license="MIT",
    packages=find_packages(where="src/python"),
    package_dir={"": "src/python"},
    package_data={"": ["etc/*", "bin/*"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Database",
    ],
    install_requires=requirements,  # Use requirements from requirements.txt
    python_requires=">=3.8",
    url="https://github.com/dmwm/T0",
)

