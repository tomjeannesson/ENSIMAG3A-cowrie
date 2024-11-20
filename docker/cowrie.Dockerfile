FROM cowrie/cowrie

COPY ./cowrie/config/cowrie.cfg /cowrie/cowrie-git/etc/cowrie.cfg
COPY ./cowrie/config/userdb.txt /cowrie/cowrie-git/etc/userdb.txt