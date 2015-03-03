from setuptools import setup, find_packages


setup(
    name='flask_json_multidict',
    version='1.0.0',
    description='Convert Flask\'s `request.get_json` dict into a MultiDict like `request.form`',
    long_description=open('README.rst').read(),
    keywords=[
        'flask',
        'request',
        'json',
        'multidict',
        'form'
    ],
    author='Todd Wolfson',
    author_email='todd@twolfson.com',
    url='https://github.com/underdogio/flask-json-multidict',
    download_url='https://github.com/underdogio/flask-json-multidict/archive/master.zip',
    packages=find_packages(),
    license='MIT',
    install_requires=open('requirements.txt').readlines(),
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
