# Usage

To properly use bacchus, you'd need:

- A domain name bought from [ghandi][1]
- A home server with docker, docker-compose and python3.8

After installing, following the ReadMe instructions, you'd just need to get
your gandi.net API key, it's located under "User Settings" / "Change Passwords
and configure access restrictions". 

<span style="display:block;text-align:center">![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/gandi.png)</span>

After having your API KEY, you can execute bacchus.

```bash
bacchus install domain.com your_email@your_provider user_nextcloud_pass API_KEY
```

This will try to auto-detect your network interface thus internal IP address, you can specify it manually if required:

```bash

bacchus install domain.com your_email@your_provider user_nextcloud_pass API_KEY ens3
```

After executing bacchus install, you'll be able to access your nextcloud with
the bacchus-provided password (you'll see it on the screen) as the user
"admin", or with your email and password

It would also have created a certificate on letsencrypt, associated to given
e-mail address, so you'll have legitimate ssl certificates.

Finally, it will configure OpenVPN, but you need to NAT yourself on your
router, the OpenVPN port (1194) on both tcp and udp, then copy the OpenVPN
produced configuration to your devices (i.e, your phone).


## Results
You can access via https, to https://private.your_server.com to the nextcloud
instance, 

You can also see, that transmission-web should be available (tough not linked
in nextcloud) at https://private.yourserver/transmission/web. 

![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/main.png)
![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/jeyllyfin.png)
![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/radar.png)
![](https://raw.githubusercontent.com/XayOn/bacchus/develop/docs/music.png)

[1]: https://ghandi.net
