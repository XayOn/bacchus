# Bacchus

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
- Download all of them! :heavy_check_mark:
- Synchronize your calendars :heavy_check_mark:
- Synchronize your contacts :heavy_check_mark:
- Synchronize your SMS :heavy_check_mark:
- Password management and synchronization  :heavy_check_mark:
- TODO list  :heavy_check_mark:
- Post-its like notes  :heavy_check_mark:
- Kanban board :heavy_check_mark:
- Edit online your documents, spreadsheets, full office solution :heavy_check_mark:
- Synchronise your health tracking apps :heavy_check_mark:

# Android support

- Handle your media using jellyfin `<https://jellyfin.io>`_
- Sync calendars and contacts with `Davx⁵ <https://www.davx5.com>`_
- Manage your passwords with `KeePassDroid <http://www.keepassdroid.com/>`_ 
- Keep your todo lists with `OpenTasks <https://opentasks.app/>`_
- Manage your kanban with `Deck <https://f-droid.org/en/packages/it.niedermann.nextcloud.deck/>`_
- Edit your documents with `AndrOpenoffice <https://play.google.com/store/apps/details?id=com.andropenoffice&hl=en_US>`_
- Save your post-its (google keep-like) with `Carnet <https://www.f-droid.org/en/packages/com.spisoft.quicknote/>`_ 
- Monitor your torrent downloads with `Tremotesf <https://f-droid.org/en/packages/org.equeim.tremotesf/>`_ 
- `Etar <https://f-droid.org/en/packages/ws.xsoh.etar/>`_ for calendar and calendar widgets.
- Keep track of your health and sync it with nextcloud with
  `OpenScale <https://f-droid.org/en/packages/com.health.openscale/>`_, `GadgetBridge <https://www.f-droid.org/en/packages/nodomain.freeyourgadget.gadgetbridge/>`_ and `Food Tracker <https://f-droid.org/en/packages/org.secuso.privacyfriendlyfoodtracker/>`_
- Keep your notes with `Nextcloud Notes <https://www.f-droid.org/en/packages/it.niedermann.owncloud.notes/>`_
- Sync your SMS with  `Nextcloud SMS <https://f-droid.org/en/packages/fr.unix_experience.owncloud_sms/>`_
- Connect to your local network from everywhere with <`OpenVPN <https://f-droid.org/en/packages/de.blinkt.openvpn/>`_

# Browser support

Most of the features are directly available within your browser on your
configured domain, with SSL. Except password sync, you can achieve that by
configuring `<https://addons.mozilla.org/en-US/firefox/addon/keepass-tusk/>
Firefox Tusk add-on`_


# Apps that provide the real services

- `LazyLibrarian <https://lazylibrarian.gitlab.io>`_
- `Radarr <https://radarr.video>`_
- `Lidarr https://lidarr.audio>`_
- `Medussa <https://pymedusa.com>`_
- `Jackett <https://github.com/Jackett/Jackett>`_ 
- `Transmission <https://transmissionbt.com/>`_
- `Nextcloud <https://nextcloud.com>`_
- `OnlyOffice <https://onlyoffice.com>`_
- `OpenVPN <https://openvpn.net>`_

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
