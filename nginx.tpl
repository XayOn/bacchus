user  www-data;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {{
    worker_connections  1024;
}}

http {{

    upstream plex {{
        server plex:32400;
    }}

    upstream lidarr {{
      server lidarr:8686;
    }}

    upstream backend {{
      server nextcloud:9000;
    }}

    upstream medusa {{
      server medusa:8081;
    }}

    upstream lazylibrarian {{
      server lazylibrarian:5299;
    }}

    upstream radarr {{
      server radarr:7878;
    }}

    upstream jackett {{
      server jackett:9117;
    }}

    upstream onlyoffice-document-server {{
      server onlyoffice-document-server; 
    }}




    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    map $http_host $this_host {{
        "" $host;
        default $http_host;
    }}

    map $http_x_forwarded_proto $the_scheme {{
        default $http_x_forwarded_proto;
        "" $scheme;
    }}

    map $http_x_forwarded_host $the_host {{
       default $http_x_forwarded_host;
       "" $this_host;
    }}

    server {{

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

        index index.php;
        error_page 403 /core/templates/403.php;
        error_page 404 /core/templates/404.php;

        rewrite ^/.well-known/carddav /remote.php/dav/ permanent;
        rewrite ^/.well-known/caldav /remote.php/dav/ permanent;

        ssl_certificate /etc/certs/{domain}/fullchain.pem;
        ssl_certificate_key /etc/certs/{domain}/privkey.pem;

        location = /robots.txt {{
            allow all;
            log_not_found off;
            access_log off;
        }}

        location ~ ^/(build|tests|config|lib|3rdparty|templates|data)/ {{
            deny all;
        }}

        location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console) {{
            deny all;
        }}

        location / {{
            rewrite ^/remote/(.*) /remote.php last;
            rewrite ^(/core/doc/[^\/]+/)$ $1/index.html;
            try_files $uri $uri/ =404;
        }}

    location ~* ^/music/ {{
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
        }}
    
    location ~* ^/books/ {{
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
        }}

    
    location ~* ^/movies/ {{
        rewrite /movies/(.*) /$1  break;
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
        }}
        
    location ~* ^/trackers/ {{
        rewrite /trackers/(.*) /$1  break;
                proxy_pass http://jackett; 
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
        }}

    
    location ~* ^/tv/ {{
        rewrite /tv/(.*) /$1  break;
                proxy_pass http://medusa; 
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
        }}
    
    location ~* ^/plex/ {{
        rewrite /tv/(.*) /$1  break;
                proxy_pass http://plex;
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
        }}

    location ~* ^/ds-vpath/ {{
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
        }}

        location ~ \.php(?:$|/) {{
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;
            fastcgi_param HTTPS off;
            fastcgi_param modHeadersAvailable true; #Avoid sending the security headers twice
            fastcgi_pass backend;
            fastcgi_intercept_errors on;
        }}

        # Adding the cache control header for js and css files
        # Make sure it is BELOW the location ~ \.php(?:$|/) {{ block
        location ~* \.(?:css|js)$ {{
            add_header Cache-Control "public, max-age=7200";
            # Add headers to serve security related headers
            add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload;";
            add_header X-Content-Type-Options nosniff;
            add_header X-Frame-Options "SAMEORIGIN";
            add_header X-XSS-Protection "1; mode=block";
            add_header X-Robots-Tag none;
            add_header X-Download-Options noopen;
            add_header X-Permitted-Cross-Domain-Policies none;
            # Optional: Don't log access to assets
            access_log off;
        }}

        # Optional: Don't log access to other assets
        location ~* \.(?:jpg|jpeg|gif|bmp|ico|png|swf)$ {{
            access_log off;
        }}

    }}
}}
