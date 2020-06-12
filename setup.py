from setuptools import setup


with open("README.md") as file:
    long_description = file.read()


setup(
    name="pg_scrubfu",
    version="0.1.0",
    description="PostgreSQL data obfuscation Kung Fu for DBA's and DevOps Masters written in Python",
    long_description=long_description,
    long_description_content_type="text/x-md",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development",
    ],
    keywords="postgres data obfuscation",
    url="https://github.com/Cyber-Mint/pg_scrubfu",
    author="Bank-Builder",
    author_email="bank-builder@cyber-mint.com",
    license="MIT",
    packages=["scrubfu"],
    install_requires=["Faker",],
    include_package_data=True,
    entry_points={"console_scripts": ["pg_scrubfu=scrubfu.pg_scrubfu:cli"],},
    zip_safe=False,
    python_requires=">=3.6",
)
