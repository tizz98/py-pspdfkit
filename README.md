# PSPDFKit API wrapper
`py-pspdfkit` is a simple API wrapper for [PSPDFKit](https://pspdfkit.com/). ![travis](https://api.travis-ci.org/tizz98/py-pspdfkit.svg?branch=master)

## Installation
`pip install py-pspdfkit`

## Usage
```python
from pspdfkit import API
client = API('http://localhost:5000', 'secret')
client.upload_file_from_url(
    'https://isotropic.org/papers/chicken.pdf',
    'cc90ea63a926fe36a9c92fab0ca246db40f34e39170764153c13e427e4acc1fb'
)
```

## Web application examples

- [Django](https://github.com/tizz98/pspdfkit-server-example-django)
