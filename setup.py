from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="KaiheilaCardBuilder",
    version="1.0.0",
    author="DancingSnow",
    author_email="1121149616@qq.com",
    description="一个构建开黑啦卡片的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DancingSnow0517/KaiheilaCardBuilder",
    project_urls={
        "Bug Tracker": "https://github.com/DancingSnow0517/KaiheilaCardBuilder/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires=">=3.6",
)
