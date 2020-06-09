from setuptools import setup


with open("README.rst") as file:
    long_description = file.read()


setup(
    name="py_app_package",
    version="0.1.9",
    description="A packaging template application ",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development",
    ],
    keywords="python package template",
    url="https://github.com/Cyber-Mint/py_app_package",
    author="Bank-Builder",
    author_email="bank-builder@cyber-mint.com",
    license="MIT",
    packages=["app"],
    install_requires=["Faker",],
    include_package_data=True,
    entry_points={"console_scripts": ["app-cli=app.app_cli:main"],},
    zip_safe=False,
    python_requires=">=3.6",
)
