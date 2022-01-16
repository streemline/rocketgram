# Copyright (C) 2015-2022 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


import asyncio
import logging
import uuid
from json import JSONDecodeError

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from .connector import Connector
from ..api import Request, Response
from ..errors import RocketgramNetworkError, RocketgramParseError

try:
    import ujson as json
except ImportError:
    import json

logger = logging.getLogger('rocketgram.connectors.tornado')


class TornadoConnector(Connector):
    __slots__ = ('_api_url', '_api_file_url', '_client', '_timeout')

    def __init__(self, *, timeout: int = 35, api_url: str = Connector.API_URL,
                 api_file_url: str = Connector.API_FILE_URL):
        super().__init__(timeout=timeout, api_url=api_url, api_file_url=api_file_url)
        self._client = AsyncHTTPClient()

    async def init(self):
        pass

    async def shutdown(self):
        pass

    async def send(self, token: str, request: Request) -> Response:
        try:
            url = self._api_url % token + request.method

            request_data = request.render()

            files = request.files()

            if len(files):
                boundary = uuid.uuid4().hex

                async def producer(write):
                    for name, field in request_data.items():
                        if isinstance(field, (dict, list, tuple)):
                            content_type = 'application/json'
                            data = json.dumps(field)
                        else:
                            content_type = 'text/plain'
                            data = str(field)

                        buf = f'--{boundary}\r\n' \
                              f'Content-Disposition: form-data; name="{name}"\r\n' \
                              f'Content-Type: {content_type}\r\n\r\n' \
                              f'{data}' \
                              f'\r\n'

                        await write(buf.encode())
                        continue

                    for fl in files:
                        begin = f'--{boundary}\r\n' \
                                f'Content-Disposition: form-data; name="{fl.file_name}"; ' \
                                f'filename="{fl.file_name}"\r\n' \
                                f'Content-Type: {fl.content_type}\r\n' \
                                f'\r\n'

                        await write(begin.encode())

                        while True:
                            chunk = fl.data.read(8 * 1024)
                            if not chunk:
                                break
                            await write(chunk)

                        await write('\r\n'.encode())

                    await write(f'--{boundary}--\r\n\r\n'.encode())

                headers = {
                    'Content-Type': f'multipart/form-data; boundary={boundary}',
                    'User-Agent': self.USER_AGENT
                }

                req = HTTPRequest(url, method='POST', headers=headers, body_producer=producer,  # noqa
                                  request_timeout=self._timeout)
            else:
                req = HTTPRequest(url, method='POST', headers=self.HEADERS, body=json.dumps(request_data),
                                  request_timeout=self._timeout)

            response = await self._client.fetch(req, raise_error=False)

            return Response.parse(json.loads(response.body), request)
        except JSONDecodeError as e:
            raise RocketgramParseError(e)
        except asyncio.CancelledError:
            raise
        except Exception as error:
            raise RocketgramNetworkError(error) from error
