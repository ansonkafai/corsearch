import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# ref:
# - https://www.blog.pythonlibrary.org/2021/09/23/python-101-how-to-create-a-python-package/
#
# notes:
# - first step:
#   The first step in this code is to import setuptools.
#   Then you read in your README.md file into a variable that you will use soon.
#   The last bit is the bulk of the code.
#   Here you call setuptools.setup(), which can take in quite a few different arguments.
#   The example below is only a sampling of what you can pass to this function.
#   To see the full listing, you'll need to go here:
#   - https://packaging.python.org/guides/distributing-packages-using-setuptools/
# - find_packages():
#   Most of the arguments are self-explanatory. Let's focus on the more obtuse ones.
#   The packages arguments is a list of packages needed for your package.
#   In this case, you use find_packages() to find the necessary packages for you automatically.
# - classifiers:
#   The classifiers argument is used for passing additional metadata to pip.
#   For example, this code tells pip that the package is Python 3 compatible.
#   Now that you have a setup.py, you are ready to create a Python wheel!

setuptools.setup(
    name="corsearch-challenge",
    version="0.0.1",
    author="Anson",
    author_email="",
    description="Corsearch challenge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.4',
)
