Bacchus
-------

Easy-enough personal cloud with media management and auto-downloads.

This proyect aims to make personal cloud and media management solutions more
widely accesible, or at least a bit more painless to setup 

To do so, it exposes a few services under the same subdomain, with a self-signed ssl
certificate and proxy-pass directives.

Launching with docker-compose:

- Lazylibrarian (Automatic torrent download and sorting of books)
- radarr (Automatic torrent download and sorting of movies)
- lidarr (Automatic torrent download and sorting of music)
- pymedussa (Automatic torrent download and sorting of tv shows)
- jackett (torrent searcher, multi-tracker)
- Transmission-daemon (torrent download)
- Nextcloud (personal cloud solution) 
- onlyoffice (online office solution)
- Home-assistant (personal domotics)

TODO List
---------

- Add VPN support, so we need only to allow access to the VPN from the outside world
- Automatically centralize links on nextcloud instance. 
- Automatically configure all services to see between themselves, for example
  radarr, lidarr and medussa with jaccket and transmission
- Pre-configure a set of trackers on Jackett.
- Add links to services on service list in Readme
- Add a Pihole, and set VPN so that its clients will always use pihole as dns server 
- Maybe some way to auto-configure those android apps? Maybe pre-create
  application passwords for the main account, and add something to do the same
  to extra accounts automatically 
- Mycroft?
- Add links to Android apps:

  + AndOpenoffice 
  + Nextcloud (file sync, photo sync (google photos), backups)
  + Davx5 (calendars and contacts sync with nextcloud)
  + Keepass and Authenticator (Google-passwords like app, sync with nextcloud)
  + Deck (trello-like app on nextcloud)
  + Carnet (Google-keep like app on nextcloud)
  + Plex (Netflix-like app)
  + OpenVPN (VPN)
  + Transmission-remote (Torrents)
  + Etar (Google-Calendar like app)
  + OpenScale, GadgetBridge and FoodTracker (open source apps that mostly replace google fit features) 
  + Nextcloud Notes app (Google-notes like app)
  + SMS for nextcloud (Google messages like app)

