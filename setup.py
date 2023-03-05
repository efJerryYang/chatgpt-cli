import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    install_requirements = f.readlines()

setuptools.setup(
    name="chatgpt-cli",
    version="0.1.0",
    author="Jerry Yang",
    author_email="efjerryyang@outlook.com",
    description="A markdown-supported command-line interface tool that connects to ChatGPT using OpenAI's API key.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/efJerryYang/chatgpt-cli/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requirements,
    entry_points={"console_scripts": ["chatgpt-cli=chatgpt_cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
