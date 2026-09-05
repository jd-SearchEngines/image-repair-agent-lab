from setuptools import find_packages, setup

setup(
    name="image-repair-agent-lab",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=["Pillow>=9.0", "numpy>=1.23"],
)
