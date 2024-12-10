from setuptools import setup, find_packages

setup(
    name='triangles_action_space',
    version='0.0.1',
    packages=find_packages(),
    description='A package for triangular game mode.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],  # Load dependencies from requirements.txt

)
