#!/bin/sh
# Crea un database separato per i test, così i test non toccano i dati veri.
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" <<SQL
CREATE DATABASE IF NOT EXISTS whoswho_test;
GRANT ALL PRIVILEGES ON whoswho_test.* TO '$MYSQL_USER'@'%';
FLUSH PRIVILEGES;
SQL
