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
  for music, [sonarr][9] for tv, [readarr][26] for books and audiobooks
- Torrent management [Prowlarr][6] for torrent searches and [Transmission][7] to
  download them. 
- Automatic subtitles downloads with [Bazarr][27]

## Media management and playback


- [Jellyfin][13] Complete Media system
- [Jellyseer][28] Web interface for media (audio, movies, series) requests.

## Cloud

Preconfigured nextcloud for all your basic needs.

- [Nextcloud][8] (files, calendar, contacts...)
- [Kiwix][29] Wikipedia, OpenStreetMap, Wikihow, complete local copies
- [SelfOss][30] Web rss aggregator, with multiple mobile applications available

## Utilities

With wireguard for connectivity, pihole to remove ads, and organizr as *the*
main screen.

- [Homarr][21] (Main page)
- [Wireguard][10] (to securely connect to your home server from outside)
- [Adguard][14] (removes most ads)
- [Watchtower][20] (Manage docker updates)
- [DashDot][31] Basic system status page
- [WebSSH][32] Allows ssh access from outside your network via wireguard vpn

## Chat

With Element, matrix and mautrix-\* bridges, you can connect to all your
favourite chat networks and use a single (element) app.

- [Matrix][23] (Matrix secure, federated IM server) - Federation won't be available
- [Element][24] (Matrix web interface)
- [Mautrix][25] (Links to other chat applications, signal, telegram, facebook, whatsapp, linkedin, twitter, slack)

## Extras

- Bacchus sets up your domains and SSL for you, using traefik and lexicon
- Bacchus sets public trackers on all the arrs

## Install 

You can either manually install pwgen and bacchus (use your favourite package
manager to install pwgen, then pip install bacchus for bacchus), or use docker:

```
	docker run -v /var/run/docker:/var/run/docker XayOn/bacchus
```
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
- [X] Setup traefik with all the services configured as subdomains
- [ ] Configure element.io riot and matrix
- [ ] Setup the arrs with prowlarr, and sync the providers
- [ ] Auto-configure organizr with all the services 
- [ ] Auto-configure mautrix clients
- [ ] Setup transmission-daemon client on the arrs


[1]: https://github.com/nextcloud/nextcloud
[3]: https://radarr.video
[4]: https://lidarr.audio
[5]: https://sonarr.tv
[6]: https://github.com/Prowlarr/Prowlarr
[7]: https://transmissionbt.com
[8]: https://nextcloud.com
[9]: https://sonarr.tv
[10]: https://www.wireguard.com/
[12]: https://kodi.tv
[13]: https://jellyfin.org
[14]: https://github.com/AdguardTeam/AdGuardHome 
[20]: https://github.com/containrrr/watchtower
[21]: https://homarr.dev/
[23]: https://matrix.org
[24]: https://element.io/
[25]: https://docs.mau.fi/bridges/
[26]: readarr
[27]: bazarr
[28]: https://github.com/Fallenbagel/jellyseerr
[29]: https://www.kiwix.org/en/
[30]: https://selfoss.aditu.de/
[31]: https://github.com/MauriceNino/dashdot
[32]: https://hub.docker.com/r/snsyzb/webssh
