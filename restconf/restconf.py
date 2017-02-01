# -*- coding: utf-8 -*-

import logging
import pathlib

import requests
from requests.auth import HTTPBasicAuth

from .configuration_file import ConfigurationFile

logger = logging.getLogger(__name__)


class RestConf(object):
    _default_header = {
        'Content-Type': 'application/vnd.yang.data+json',
        'Accept': 'application/vnd.yang.api+json'
    }
    _default_context = 'operational'

    def __init__(self, username=None, password=None,
                 hostname=None, port=None, ssl=None, verify=None):
        username = username or self._get_config('credentials', 'username')
        password = password or self._get_config('credentials', 'password')
        auth = HTTPBasicAuth(username, password)
        hostname = hostname or self._get_config('system', 'hostname')
        port = port or self._get_config('system', 'port') or 8008
        if verify is None:
            verify = self._get_config('security', 'verify')
        if verify is None:
            verify = True
        if ssl is None:
            ssl = self._get_config('security', 'ssl').lower() == 'true'
        protocol = 'https'
        if ssl is False:
            protocol = 'http'

        self._url = '{}://{}:{}'.format(protocol, hostname, port)
        self._standard_headers = {
            'verify': verify,
            'headers': self._default_header,
            'auth': auth,
        }

    def _get_config(self, section, value):
        if not hasattr(self, '_config_file'):
            config_file = str(pathlib.Path().home() / '.restconfrc')
            self._config_file = ConfigurationFile.get(config_file)
        section = self._config_file.get(section)
        if section is not None:
            return section.get(value)

    @property
    def version(self):
        if not hasattr(self, '_api_version'):
            self.roots
        return self._api_version

    @property
    def context(self):
        if not hasattr(self, '_context'):
            self._context = self._default_context
        return self._default_context

    def get_contexts(self):
        if not hasattr(self, '_contexts'):
            default_headers = self._default_header.copy()
            default_headers['Accept'] = 'application/vnd.yang.api+json'

            headers = self._standard_headers.copy()
            headers['headers'] = default_headers

            response = requests.get(
                '/'.join([self._url, 'api?verbose']),
                **headers
            )
            contexts = dict()
            root_keys = ('conifg', 'running', 'operational', 'rollbacks')
            data = response.json()['api']
            for key, value in data.items():
                if key in root_keys:
                    contexts[key] = value['_self']
            self._api_version = data['version']
            self._contexts = contexts
        return self._contexts

    def _context_uri(self, context=None):
        contexts = self.get_contexts()
        context = context or self.context
        uri = '/'.join([
            self._url,
            contexts[self.context].lstrip('/'),
        ])
        return uri

    @property
    def capabilities(self):
        if not hasattr(self, '_capabilities'):
            response = requests.get(
                '/'.join([
                    self._context_uri(context='operational'),
                    'netconf-state',
                    'capabilities'
                ]),
                **self._standard_headers
            )
            import ipdb; ipdb.set_trace()
            capabilities = response.json()['ietf-netconf-monitoring:capabilities']['capability']
            self._capabilities = capabilities
        return self._capabilities
