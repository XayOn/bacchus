<span style="display:block;text-align:center">[![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/bacchus.png)](https://github.com/XayOn/bacchus) </span>

## Keep your data to yourself

Bacchus helps you configure a set of self-hosted tools that would allow you to
live without big corporations, while keeping your data secure.

All the services will only be available on your home network, a VPN server
is setup and a client configuration file is automatically issued upon
installation, so you only need to forward VPN port to the machine where you've
got bacchus installed trough your router.

Ultimately, bacchus works around [NextCloud][1], adding custom links inside (as
iframes) to external tools (like media management and automated
episode/movies/books downloads)

:warning: :computer: Note that you need a certain technical knowledge to run this.
You should at least be confortable with docker, linux and a bit on the linux CLI.

## :computer: What will I get?

**Bacchus sets, configures and manages up the following applications**

## Media management and download

- [LazyLibrarian][2] (books download and management)
- [Radarr][3] (movies download and management)
- [Lidarr][4] (audio download and management)
- [Medussa][5] (series downloads and management)
- [Jackett][6] (torrent tracker search management)
- [Transmission][7] (torrent downloads)

## Media management and playback

- [kodi][12] (media player, tv-like)
- [Jellyfin][13] (media player, android/web, integration with kodi available)

## Cloud

- [Nextcloud][8] (files, calendar, contacts...)
- [OnlyOffice][9] (online office suite)

## Utilities

- [OpenVPN][10] (to securely connect to your home server from otside)
- [PiHole][14] (remove internet advertisings)

And links them inside nextcloud for a seamless user experience. 

## Install 

Bacchus is provided as a python executable, you can, for example, install it with pip as user:

```bash
pip install --user bacchus
```

See [usage documentation][11] for more.


[1]: https://github.com/nextcloud/nextcloud
[2]: https://lazylibrarian.gitlab.io
[3]: https://radarr.video
[4]: https://lidarr.audio
[5]: https://pymedusa.com
[6]: https://github.com/Jackett/Jackett
[7]: https://transmissionbt.com
[8]: https://nextcloud.com
[9]: https://onlyoffice.com
[10]: https://openvpn.net
[11]: docs/usage.md
[12]: https://kodi.tv
[13]: https://jellyfin.org
[14]: https://pi-hole.net/
