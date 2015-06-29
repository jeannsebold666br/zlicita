mysql -u root --password=tux zlicita -e "truncate table coleta;"
mysql -u root --password=tux zlicita -e "truncate table registro;"
mysql -u root --password=tux zlicita < insert.sql
python3 robocoleta.py
