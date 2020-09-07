{%raw%}user  www-data;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
{%endraw%}

    {% for service, port in services.items() %}
    upstream {service} {{
        server {service}:{port};
    }} 

    {% if selected.get('NextCloud') %}{%raw%}
    upstream onlyoffice-document-server {
      server onlyoffice-document-server; 
    }
    {%endraw%}{%endif}

{%raw%}
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    map $http_host $this_host {
        "" $host;
        default $http_host;
    }

    map $http_x_forwarded_proto $the_scheme {
        default $http_x_forwarded_proto;
        "" $scheme;
    }

    map $http_x_forwarded_host $the_host {
       default $http_x_forwarded_host;
       "" $this_host;
    }


    server {
    	listen 80 default_server;
    	listen [::]:80 default_server;
    	server_name _;
    	return 301 https://$host$request_uri;
    }

    server {

    listen 443 default_server ssl;

        # Add headers to serve security related headers
        add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload;";
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header X-Robots-Tag none;
        add_header X-Download-Options noopen;
        add_header X-Permitted-Cross-Domain-Policies none;

        root /var/www/html;
        client_max_body_size 10G; # 0=unlimited - set max upload size
        fastcgi_buffers 64 4K;

        gzip off;

        index index.html;

        ssl_certificate /etc/certs/private.{domain}.crt;
        ssl_certificate_key /etc/certs/private.{domain}.key;

        location = /robots.txt {
            allow all;
            log_not_found off;
            access_log off;
        }

        location ~ ^/(build|tests|config|lib|3rdparty|templates|data)/ {
            deny all;
        }

        location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console) {
            deny all;
        }

        rewrite ^/.well-known/carddav /remote.php/dav/ permanent;
        rewrite ^/.well-known/caldav /remote.php/dav/ permanent;

        {%endraw%}{% if 'Lidarr' in selected %}{%raw%}
        location ~* ^/music/ {
            rewrite /lidarr/(.*) /$1  break;
            proxy_pass http://lidarr;
            proxy_redirect     off;
            client_max_body_size 100m;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $the_host/ds-vpath;
            proxy_set_header X-Forwarded-Proto $the_scheme;
        }
        {%endraw%}{%endif%}

        {% if 'Transmission' in selected %}{%raw%}
        location ^~ /transmission {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-NginX-Proxy true;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_pass_header X-Transmission-Session-Id;
            add_header   Front-End-Https   on;
            
            location /transmission/rpc {
                proxy_pass http://transmission;
            }
            
            location /transmission/web/ {
                proxy_pass http://transmission;
            }
            
            location /transmission/upload {
                proxy_pass http://transmission;
            }
        }
        {%endraw%}{%endif%}

        {% if 'LazyLibrarian' in selected %}{%raw%}
        location ~* ^/books/ {
            rewrite /books/(.*) /$1  break;
            proxy_pass http://lazylibrarian;
            proxy_redirect     off;
            client_max_body_size 100m;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $the_host/ds-vpath;
            proxy_set_header X-Forwarded-Proto $the_scheme;
        }
        {%endraw%}{%endif%}

        {% if 'Radarr' in selected %}{%raw%}
        location ~* ^/movies/ {
            proxy_pass http://radarr;
            proxy_redirect     off;
            client_max_body_size 100m;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $the_host/ds-vpath;
            proxy_set_header X-Forwarded-Proto $the_scheme;
        }
        {%endraw%}{%endif%}

        {% if 'Jackett' in selected %}{%raw%}
        location ~* ^/trackers/ {
           proxy_pass http://jackett; 
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_set_header X-Forwarded-Host $http_host;
           proxy_redirect off;
        }
        {%endraw%}{%endif%}

        {% if 'Medusa' in selected %}{%raw%}
        location ~* ^/tv/ {
            proxy_pass http://medusa; 
            proxy_redirect     off;
            client_max_body_size 100m;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $the_host;
            proxy_set_header X-Forwarded-Proto $the_scheme;
        }
        {%endraw%}{%endif%}

        {% if 'Jellyfin' in selected %}{%raw%}
        location /jellyfin/ {
            proxy_pass http://jellyfin;
            proxy_pass_request_headers on;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $http_host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
        }
        {%endraw%}{%endif%}

        {% if 'PiHole' in selected %}{%raw%}
        location /pihole/ {
            proxy_pass http://pihole;
            proxy_pass_request_headers on;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $http_host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $http_connection;
        }
        {%endraw%}{%endif%}
        
        {% if 'NextCloud' in selected %}{%raw%}
        // NextCloud is actually mandatory
        location ~* ^/ds-vpath/ {
            rewrite /ds-vpath/(.*) /$1  break;
            proxy_pass http://onlyoffice-document-server;
            proxy_redirect     off;

            client_max_body_size 100m;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $the_host/ds-vpath;
            proxy_set_header X-Forwarded-Proto $the_scheme;
        }
        {%endraw%}{%endif%}

        {% if 'Kodi' in selected %}{%raw%}
        location /kodi {
            rewrite /kodi/(.*) /$1  break;
            proxy_pass         http://kodi;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Server $host;
            proxy_set_header   X-Forwarded-Host $server_name;
        }

        location /jsonrpc {
            proxy_pass         http://kodi;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Server $host;
            proxy_set_header   X-Forwarded-Host $server_name;
        }
        {%endraw%}{%endif%}

        location / {
            proxy_headers_hash_max_size 512;
            proxy_headers_hash_bucket_size 64;

            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

                add_header Content-Security-Policy "None";
            proxy_hide_header Content-Security-Policy;

            add_header Front-End-Https on;
            proxy_pass http://nextcloud/;
        }

        location ~* \.(?:jpg|jpeg|gif|bmp|ico|png|swf)$ {
            access_log off;
        }
    }
}
