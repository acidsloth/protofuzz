#/bin/bash
openssl req -x509  -days 15340 -newkey rsa:2048 -out localhost.crt -keyout localhost.key && cat localhost.key localhost.crt > localhost.pem
