
# TODO: tail (-f?) option to not restart suggested during masters presentation

# TODO: if mac, if linux (access.log or access_log) for github
rm -f access.log
rm /var/log/apache2/access.log
rm /var/log/apache2/error.log
touch /var/log/apache2/access.log

nano /var/log/apache2/access.log
