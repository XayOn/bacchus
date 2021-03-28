<span style="display:block;text-align:center">[![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/bacchus.png)](https://github.com/XayOn/bacchus) </span>


## Keep your data to yourself

Bacchus helps you configure a set of self-hosted tools that would allow you to
live without big corporations, while keeping your data secure. Save hours
setting up your cloud and media services.

All the services will only be available on your home network, a wireguard
server is setup and a client configuration file is automatically issued upon
installation, so you only need to forward VPN port to the machine where you've
got bacchus installed trough your router.

![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/main.png)

## :computer: What will I get?

**Bacchus sets, configures and manages up the following applications**

## Media download

- The \*arrs for media download management. [Radarr][3] for movies, [Lidarr][4] for music, [sonarr][9] for tv 
- Torrent management [Jackett][6] for torrent searches and [Transmission][7] to download them. 

## Media management and playback

- [kodi][12] Home Theather
- [Jellyfin][13] Complete Media system

## Cloud

- [Nextcloud][8] (files, calendar, contacts...)

## Utilities

- [Wireguard][10] (to securely connect to your home server from otside)
- [PiHole][14] (remove internet advertisings)
- [Watchtower][20] (Manage docker updates)
- [Organizr][21] (Main page)

## Extras

- Baccus sets up your domains and SSL for you, using traefik and lexicon

And links them inside nextcloud for a seamless user experience. 
Bacchus sets up a set of default public trackers on jackett and the arrs.

## Install 

Bacchus has a two-stages installation, first, you need to create a custom .env file. 
In a near future this will be automated. Have a look at docs/examples directory.
Then, execute the install.sh script

It does not require any dependencies other than docker-compose and bash.

See [usage documentation][11] for more.


[1]: https://github.com/nextcloud/nextcloud
[2]: https://lazylibrarian.gitlab.io
[3]: https://radarr.video
[4]: https://lidarr.audio
[5]: https://sonarr.tv
[6]: https://github.com/Jackett/Jackett
[7]: https://transmissionbt.com
[8]: https://nextcloud.com
[9]: https://sonarr.tv
[10]: https://openvpn.net
[11]: docs/usage.md
[12]: https://kodi.tv
[13]: https://jellyfin.org
[14]: https://pi-hole.net/
[20]: https://github.com/containrrr/watchtower
[21]: https://ombi.io
