#!/usr/bin/env python

"""
Netdata plugin to pull statistics from a FXserver (FiveM, RedM).

The MIT License (MIT)
Copyright (c) 2021 Aurélien Janvier

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# @Title            : fxserver.chart
# @Description      : Netdata plugin to pull statistics from a FXserver (FiveM, RedM)
# @Author           : Aurélien Janvier
# @Email            : dev (at) ajanvier.fr
# @Copyright        : Copyright (C) 2021 Aurélien Janvier
# @License          : MIT
# @Maintainer       : Aurélien Janvier
# @Date             : 2021-10-02
# @Version          : 1.0
# @Status           : stable
# @Usage            : Automatically processed by netdata
# @Notes            : With default NetData installation put this file under
#                   : /usr/libexec/netdata/python.d/ and the config file under
#                   : /etc/netdata/python.d/
# @Python_version   : >3.6.2 or >2.7.3
"""

import json
import os

from bases.FrameworkServices.UrlService import UrlService

# Basic plugin settings for netdata.
update_every = 1
priority = 60000
retries = 10

ORDER = ['players']

CHARTS = {
    'players': {
        'options': [None, 'Players online', 'players', 'Players', 'fxserver.connected_player', 'line'],
        'lines': [
            ['connected_players', 'online', 'absolute']
        ]
    }
}

class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        
        self.order = ORDER
        self.definitions = CHARTS

        self.host = self.configuration.get('host', '127.0.0.1')
        self.port = self.configuration.get('port', 30120)

        self.url = 'http://{host}:{port}/dynamic.json'.format(host=self.host, port=self.port)

    def check(self):
        """
        Parse configuration and check if local FXserver server is running
        :return: boolean
        """

        try:
            if self.url == '':
                raise KeyError

        except KeyError:
            self.error("Please specify a FXserver URL inside the fxserver.conf!", "Disabling plugin...")

            return False

        # Check once if FXserver is running when host is localhost.
        if self.host in ['localhost', '127.0.0.1']:
            FXserver_running = False

            pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

            for pid in pids:
                try:
                    if b'FXServer' in open(os.path.join('/proc', pid, 'cmdline').encode(), 'rb').read():
                        FXserver_running = True
                        break

                except IOError as e:
                    self.error(e)

            if FXserver_running is False:
                self.error("No local FXserver running. Disabling plugin...")

                return False

            else:
                self.debug("FXserver process found. Connecting...")

        UrlService.check(self)
        return True

    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """
        try:
            data = json.loads(self._get_raw_data())
            return {'connected_players': int(data['clients'])}
        except (ValueError, AttributeError) as e:
            self.error(e)
            return None