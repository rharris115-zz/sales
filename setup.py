from setuptools import find_packages, setup

setup(
    name='sales',
    version='0.1.0',
    description='A tool to persist and analyze sales data.',
    author='Richard Harris',
    author_email='richard.w.harris@mac.com',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'pytest', 'click', 'SQLAlchemy', 'pytz'
    ],
    entry_points={
        'console_scripts': [
            'import-sales=src.import_main:main',
        ]
    }
)
