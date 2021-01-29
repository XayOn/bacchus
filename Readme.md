<span style="display:block;text-align:center">[![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/bacchus.png)](https://github.com/XayOn/bacchus) </span>


## Keep your data to yourself

Bacchus helps you configure a set of self-hosted tools that would allow you to
live without big corporations, while keeping your data secure. Save hours
setting up your cloud and media services.

All the services will only be available on your home network, a VPN server
is setup and a client configuration file is automatically issued upon
installation, so you only need to forward VPN port to the machine where you've
got bacchus installed trough your router.

![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/main.png)

Ultimately, bacchus works around [NextCloud][1], adding custom links inside (as
iframes) to external tools (like media management and automated
episode/movies/books downloads)

## :computer: What will I get?

**Bacchus sets, configures and manages up the following applications**

## Media download

- The \*arrs for media download management ([Radarr][3] for movies, [Lidarr][4] for music, [sonarr][9] for tv 
- Torrent management ([Jackett][6] (torrent searches), [Transmission][7] (torrent downloads))

## Media management and playback

- [ombi][21] Request movies, tv shows and music, integrates with the arrs and jellyfin
- [kodi][12] Home Theather 
- [Jellyfin][13] Complete Media system

## Cloud

- [Nextcloud][8] (files, calendar, contacts...)

## Utilities

- [OpenVPN][10] (to securely connect to your home server from otside)
- [PiHole][14] (remove internet advertisings)
- [Watchtower][20] (Manage docker updates)

And links them inside nextcloud for a seamless user experience. 

## Install 

Bacchus is provided as a python executable, you can, for example, install it with pip as user:

```bash
pip install bacchus
```

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
