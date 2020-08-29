<span style="display:block;text-align:center">[![](https://raw.githubusercontent.com/XayOn/bacchus/develop/bacchus.png)](https://github.com/XayOn/bacchus) </span>

## Keep your data to yourself

Bacchus helps you configure a comprehensible set of self-hosted tools that
would allow you to live without big corporations, while keeping your data
secure.

> You'll need to have a domain on ghandi.net and get your ghandi.net API key.

All the services will only be available on your home network, a VPN server
is setup and a client configuration file is automatically issued upon
installation, so you only need to forward VPN port to the machine where you've
got bacchus installed trough your router.

Ultimately, bacchus works around [NextCloud][1], adding custom links inside (as
iframes) to external tools (like media management).

# Features

:warning: Note that this is just an installer/bundle of the real tools that make the magic.

- Keep track, download automatically and watch online your favourite movies, tv
  shows and music :heavy_check_mark: 
- Download all of them automatically! :heavy_check_mark:
- Synchronize your calendars, contacts and SMS trough nextcloud :heavy_check_mark:
- TODO list with nextcloud :heavy_check_mark:
- Post-its notes and kanban board with nextcloud :heavy_check_mark:
- Edit online your documents, spreadsheets, full office solution :heavy_check_mark:

# :computer: Bacchus automatically sets up the following applications

- `LazyLibrarian <https://lazylibrarian.gitlab.io>`_
- `Radarr <https://radarr.video>`_
- `Lidarr https://lidarr.audio>`_
- `Medussa <https://pymedusa.com>`_
- `Jackett <https://github.com/Jackett/Jackett>`_ 
- `Transmission <https://transmissionbt.com/>`_
- `Nextcloud <https://nextcloud.com>`_
- `OnlyOffice <https://onlyoffice.com>`_
- `OpenVPN <https://openvpn.net>`_

> And links them inside nextcloud for a seamless user experience. 

# Usage

Bacchus is installed either directly with pypi

```bash
        pip install bacchus
```

Or

```bash
pip install bacchus --user
```

Or by downloading this repository and installing with poetry by executing::

        poetry install 

Afterwards, you'll have a bacchus command available.

```
    USAGE
      bacchus install [<domain>] [<username>] [<password>]
    
    ARGUMENTS
      <domain>               Domain (FQDN) for virtualhosts
      <username>             Nextcloud first user's username
      <password>             Nextcloud first user's password
    
    GLOBAL OPTIONS
      -h (--help)            Display this help message
      -q (--quiet)           Do not output any message
      -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
      -V (--version)         Display this application version
      --ansi                 Force ANSI output
      --no-ansi              Disable ANSI output
      -n (--no-interaction)  Do not ask any interactive question
```


[1]: https://github.com/nextcloud/nextcloud
