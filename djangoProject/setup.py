from setuptools import setup, find_packages

setup(
    name="djangoProject",
    version="0.1",
    author="Piotr Kosakowski, Michał Matejczuk",
    description='User interface for polygonal packit',
    long_description=open('README.md').read(),
    url='https://github.com/matejczukm/packit-polygons',
    long_description_content_type='text/markdown',
    license='MIT',
    python_requires='>=3.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.0",
        "polygonal_packit>=0.2"
    ],

)
