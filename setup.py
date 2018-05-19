from setuptools import setup

setup(
    name='har-analyze',
    version='1.0',
    packages=['har-analyze'],
    description='Simplified python library to plot HTTP Archive format Timings.',
    author='Satish Kumar Kadarkarai Mani',
    author_email='michael.satish@gmail.com',
    install_requires=[
        'click>=6.7',
        'pandas==0.23.0',
        'matplotlib==2.2.2'
    ]
)
