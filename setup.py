from setuptools import setup, find_packages

setup(
    name="python-cryptobox",
    version="0.1.0",
    description="A cffi wrapper for cryptobox-c",
    author="Alexander Eisele",
    author_email="alexander@eiselecloud.de",
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["cryptobox_build:ffi"],
    install_requires=["cffi>=1.0.0"],
    packages=find_packages()
)
