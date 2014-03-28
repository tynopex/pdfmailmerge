from setuptools import setup, find_packages

setup(
    name='pdfmailmerge',
    version='0.0.0',        # See pdfmailmerge/__init__.py

    description='PDF Mail Merge library',
    url='https://github.com/tynopex/pdfmailmerge',

    license='MIT',

    packages=find_packages(),

    install_requires=[
        'PyPDF2',
        ],
    )
