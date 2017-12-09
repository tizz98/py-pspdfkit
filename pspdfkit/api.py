import hashlib
import os

import magic
import requests


class API:
    """
    Examples
    --------
    >>> from pspdfkit import API
    >>> client = API('http://localhost:5000', 'secret')
    >>> client.upload_file_from_url(
    >>>     'https://isotropic.org/papers/chicken.pdf',
    >>>     'cc90ea63a926fe36a9c92fab0ca246db40f34e39170764153c13e427e4acc1fb'
    >>> )
    """
    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key
        self.base_url = '{}/api/'.format(self.host)

    @property
    def _headers(self):
        return {
            'Authorization': 'Token token={}'.format(self.api_key),
        }

    def upload_file_from_path(self, file_path):
        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as file_obj:
            return self.upload_file_from_obj(file_obj, file_name)

    def upload_file_from_obj(self, file_obj, file_name):
        try:
            mime_type = magic.from_buffer(file_obj.read(1024), mime=True)
        finally:
            file_obj.seek(0)

        return self._post('documents', files={
            'file': (
                file_name,
                file_obj,
                mime_type,
                {},
            ),
        })

    def upload_file_from_url(self, url, sha256):
        return self._post('documents', json={'url': url, 'sha256': sha256})

    def get_document_properties(self, document_id):
        return self._get('documents/{}/properties'.format(document_id))

    def get_source_document(self, document_id):
        return self._get('documents/{}/pdf'.format(document_id), params={
            'source': True,
        })

    def copy_document(self, document_id):
        return self._post('copy_document', json={'document_id': document_id})

    def delete_document(self, document_id):
        return self._delete('documents/{}'.format(document_id))

    @classmethod
    def sha256(cls, file_path):
        with open(file_path, 'rb') as f:
            return cls.sha256_file_obj(f)

    @classmethod
    def sha256_file_obj(cls, file_obj):
        sha256 = hashlib.sha256()
        for block in iter(lambda: file_obj.read(65536), b''):
            sha256.update(block)
        return sha256.hexdigest()

    def _get(self, endpoint, params=None, **kwargs):
        return self._request('get', endpoint, params=params, **kwargs)

    def _post(self, endpoint, data=None, json=None, **kwargs):
        return self._request('post', endpoint, data=data, json=json, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._request('delete', endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].update(self._headers)

        response = requests.request(
            method,
            '{}{}'.format(self.base_url, endpoint),
            **kwargs
        )
        response.raise_for_status()
        return response.json()
