<span style="display:block;text-align:center">[![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/bacchus.png)](https://github.com/XayOn/bacchus) </span>


## Keep your data to yourself

### :godmode: Self-host your life

Bacchus helps you configure a set of self-hosted tools that would allow you to
live without big corporations, while keeping your data secure. Save hours
setting up your cloud and media services ready and setup.

![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/main.png)

## :computer: What will I get?

**Bacchus sets, configures and manages up the following applications**

## Media download

Automatic media download for series, movies and music.

- The \*arrs for media download management. [Radarr][3] for movies, [Lidarr][4]
  for music, [sonarr][9] for tv 
- Torrent management [Jackett][6] for torrent searches and [Transmission][7] to
  download them. 

## Media management and playback

If a gles-capable screen is detected, kodi will take it over, allowing a
complete home theater experience.

- [kodi][12] Home Theather
- [Jellyfin][13] Complete Media system

## Cloud

Preconfigured nextcloud for all your basic needs.
Make sure to install colabora and colabora local server!

- [Nextcloud][8] (files, calendar, contacts...)

## Utilities

With wireguard for connectivity, pihole to remove ads, and organizr as *the*
main screen.

- [Organizr][21] (Main page)
- [Wireguard][10] (to securely connect to your home server from otside)
- [PiHole][14] (remove internet advertisings)
- [Watchtower][20] (Manage docker updates)

## Chat

With Element, matrix and mautrix-\* bridges, you can connect to all your
favourite chat networks and use a single (element) app.

- [Matrix][23] (Matrix secure, federated IM server) - Federation won't be available
- [Element][24] (Matrix interface)
- [Mautrix][25] (Links to other chat applications)

## Extras

- Bacchus sets up your domains and SSL for you, using traefik and lexicon
- Bacchus sets public trackers on all the arrs

## Install 

Bacchus has a two-stages installation, first, you need to create a custom .env file. 
In a near future this will be automated. Have a look at docs/examples directory.

Then, launch docker-compose up, wait a bit for it to populate all the services,
and restart docker compose with docker-compose restart

## :computer: Networking setup

All the services will only be available behind a wireguard server.

Bacchus **won't open any other port**, so you don't need to worry about
anything else on networking / configuration side. You need to configure NAT for
wireguard port (51820 udp) on your router, point
to your bacchus machine. 

## Features

- [X] Docker-compose based
- [X] Configure domains automatically
- [X] Configure SSL
- [X] Setup wireguard with a client
- [X] Setup postgresql
- [X] Setup nextcloud automatically
- [X] Setup KODI
- [X] Setup the arrs with jackett, and sync the providers
- [X] Setup traefik with all the services configured as subdomains
- [X] Configure element.io riot and matrix
- [ ] Auto-configure organizr with all the services 
- [ ] Auto-configure mautrix clients
- [ ] Setup transmission-daemon client on the arrs


[1]: https://github.com/nextcloud/nextcloud
[2]: https://lazylibrarian.gitlab.io
[3]: https://radarr.video
[4]: https://lidarr.audio
[5]: https://sonarr.tv
[6]: https://github.com/Jackett/Jackett
[7]: https://transmissionbt.com
[8]: https://nextcloud.com
[9]: https://sonarr.tv
[10]: https://www.wireguard.com/
[12]: https://kodi.tv
[13]: https://jellyfin.org
[14]: https://pi-hole.net/
[20]: https://github.com/containrrr/watchtower
[21]: https://organizr.app
[23]: https://matrix.org
[24]: https://element.io/
[25]: https://docs.mau.fi/bridges/
