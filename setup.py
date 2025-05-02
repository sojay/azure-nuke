from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aznuke",
    version="0.1.3",
    description="Azure resource scanner and cleanup tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Samuel Okorie",
    author_email="thesamokorie@gmail.com",  # Replace with your email
    url="https://github.com/sojay/azure-nuke",  # Replace with your repository URL
    packages=find_packages(include=["aznuke", "aznuke.*", "src", "src.*"]),
    include_package_data=True,
    package_data={
        '': ['config/*.yaml'],
    },
    install_requires=[
        "azure-identity>=1.10.0",
        "azure-mgmt-resource>=22.0.0",
        "azure-mgmt-subscription>=3.1.1",
        "azure-mgmt-compute>=27.0.0",
        "azure-mgmt-network>=22.0.0",
        "azure-mgmt-storage>=20.0.0",
        "azure-mgmt-keyvault>=10.0.0",
        "azure-mgmt-monitor>=5.0.0",
        "pyyaml>=6.0",
        "colorama==0.4.6",
        "pyfiglet==0.8.post1",
        "tqdm==4.66.1",
    ],
    entry_points={
        "console_scripts": [
            "aznuke=aznuke:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    keywords="azure, cloud, cleanup, infrastructure, devops",
    python_requires=">=3.8",
) 