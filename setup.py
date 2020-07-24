from setuptools import setup

__version__ = '0.2.5'

setup(
    name="py-pspdfkit",
    version=__version__,
    url="https://github.com/tizz98/py-pspdfkit",
    download_url="https://github.com/tizz98/py-pspdfkit/tarball/{version}".format(
        version=__version__,
    ),
    author="Elijah Wilson",
    author_email="elijah@elijahwilson.me",
    description="A simple API wrapper for PSPDFKit",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="pspdfkit pdf",
    install_requires=[
        "requests>=2.22,<3.0",
    ],
    packages=[
        "pspdfkit",
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=True,
)
