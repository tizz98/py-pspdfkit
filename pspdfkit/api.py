import hashlib
import json
import os

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
    PDF_MIME_TYPE = 'application/pdf'

    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key
        self.base_url = '{}/api/'.format(self.host)

    @property
    def _headers(self):
        return {
            'Authorization': 'Token token={}'.format(self.api_key),
            'PSPDFKit-API-Version': '2017.7',
        }

    def upload_file_from_path(self, file_path):
        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as file_obj:
            return self.upload_file_from_obj(file_obj, file_name)

    def upload_file_from_obj(self, file_obj, file_name):
        return self._post('documents', files={
            'file': (
                file_name,
                file_obj,
                self.PDF_MIME_TYPE,
                {},
            ),
        }, headers={'Content-Type': self.PDF_MIME_TYPE})

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

    def get_annotations(self, document_id, page=None):
        url_kwargs = {'page': page, 'document_id': document_id}

        if page is None:
            endpoint = 'documents/{document_id}/annotations'
        else:
            endpoint = 'documents/{document_id}/pages/{page}/annotations'

        return self._ndjson_request('get', endpoint.format(**url_kwargs))

    def add_annotation(self, document_id, annotation):
        return self._post('documents/{}/annotations'.format(document_id),
                          json=annotation)

    def update_annotation(self, document_id, annotation_id, new_data):
        return self._put(
            'documents/{}/annotations/{}'.format(document_id, annotation_id),
            json=new_data,
        )

    def delete_annotation(self, document_id, annotation_id):
        return self._delete(
            'documents/{}/annotations/{}'.format(document_id, annotation_id))

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

    def _put(self, endpoint, data=None, json=None, **kwargs):
        response = self._raw_request(
            'put', endpoint, data=data, json=json, **kwargs
        )
        response.raise_for_status()

    def _delete(self, endpoint, **kwargs):
        response = self._raw_request('delete', endpoint, **kwargs)
        response.raise_for_status()

    def _request(self, method, endpoint, **kwargs):
        response = self._raw_request(method, endpoint, **kwargs)
        response.raise_for_status()
        return response.json()

    def _raw_request(self, method, endpoint, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].update(self._headers)

        return requests.request(
            method,
            '{}{}'.format(self.base_url, endpoint),
            **kwargs
        )

    def _ndjson_request(self, method, endpoint, **kwargs):
        kwargs['stream'] = True
        kwargs.setdefault('headers', {})
        kwargs['headers']['Accept'] = 'application/x-ndjson'
        response = self._raw_request(method, endpoint, **kwargs)

        for line in response.iter_lines():
            yield json.loads(line.decode('utf-8'))
