# FXserver netdata plugin

Netdata plugin to pull statistics from a FXserver (FiveM, RedM).

## Installation ##

With your default netdata installation copy the netdata.chart.py script to
`/usr/libexec/netdata/python.d/` and the netdata.conf config file to
`/etc/netdata/python.d/`. The location of these directories may vary depending
on your distribution. Read your given release of netdata for more information.

Restart netdata to activate the plugin after you have made these changes.

To disable the FXserver plugin, edit /etc/netdata/python.d.conf and add fxserver: no.
```

## Debugging
switch to netdata user:
`sudo su -s /bin/bash netdata`

Run plugin in debug mode:
`/usr/libexec/netdata/plugins.d/python.d.plugin 1 debug trace fxserver`

## License ##

This repository is released under the MIT license. For more information please
refer to [LICENSE](https://github.com/ajanvier/netdata-fxserver/blob/master/LICENSE)