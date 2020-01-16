Bacchus
-------

Freedom for your home and media. Fast setup to a libre solution on media
manamement, torrent automatic downloads, cloud and office on-cloud.

**Tired of installing the medusa/radarr/lidarr/transmission pack?**
**What about nextcloud and onlyoffice?**

This proyect aims to make personal cloud and media management solutions more
widely accesible, or at least a bit more painless to setup 

To do so, it exposes a few services under the same subdomain, with a self-signed ssl certificate and proxy-pass directives.


Features
--------

Note that this is just an installer/bundle of the real tools that make the magic.

Keeps track and auto-downloads your favorite movies (radarr), favourite TV
Series (medusa), favorite music (lidarr) and books (lazylibrarian).
Movies, TV Series, books and music auto-download.
All with the help of Jackett and transmission daemon for torrent search and
download.

Installs your personal cloud, allowing backups and online/offline
(android/linux/windows) collaborative document editing (nextcloud +
onlyoffice), contacts syncronization, calendar synchronization, task list...

With KeePassDroid and KeePass Tusk you can sync your passwords safely between
devices.

Finally, it installs and configures a VPN server, so you just need to open the
one VPN port, and share your freshly-generated VPN config with your devices.

Currently installed apps
------------------------

- Lazylibrarian 
- radarr 
- lidarr
- pymedussa 
- jackett 
- Transmission-daemon 
- Nextcloud 
- onlyoffice
- OpenVPN


Android integration
-------------------

Recommended Android APPS

- AndOpenoffice 
- Nextcloud (file sync, photo sync (google photos), backups)
- Davx5 (calendars and contacts sync with nextcloud)
- Keepass and Authenticator (Google-passwords like app, sync with nextcloud)
- Deck (trello-like app on nextcloud)
- Carnet (Google-keep like app on nextcloud)
- Plex (Netflix-like app)
- OpenVPN (VPN)
- Transmission-remote (Torrents)
- Etar (Google-Calendar like app)
- OpenScale, GadgetBridge and FoodTracker (open source apps that mostly replace google fit features) 
- Nextcloud Notes app (Google-notes like app)
- SMS for nextcloud (Google messages like app)


Usage
-----

Bacchus is installed either directly with pypi::

        pip install bacchus

Or by downloading this repository and installing with poetry by executing::

        poetry install 

Afterwards, you'll have a bacchus command available.

::

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
