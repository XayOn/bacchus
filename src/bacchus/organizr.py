import os
from bacchus.base import HomeServerApp
import requests


class Organizr(HomeServerApp):
    def setup_first_step(self):
        password = os.getenv('NEXTCLOUD_ADMIN_PASSWORD'),
        fkey = "$2y$10$nqjRp2/xMFeDIuu5dfPKg.LiShVkhiq84P77D/owzy9yLCI2hSjHu"
        requests.post("http://organizr/api/v2/wizard",
                      data={
                          "license": "personal",
                          "username": os.getenv('NEXTCLOUD_ADMIN_USER'),
                          "email": os.getenv('email'),
                          "password": password,
                          "hashKey": password,
                          "registrationPassword": password,
                          "api": "pih3y94mznr5xbths22v",
                          "dbName": "db",
                          "dbPath": "/config/www/organizr",
                          "formKey": fkey
                      })
