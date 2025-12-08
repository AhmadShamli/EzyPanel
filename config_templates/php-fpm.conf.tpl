[{{HOSTNAME}}]
user = {{WEB_USER}}
group = {{WEB_GROUP}}
listen = {{PHP_SOCKET}}
listen.owner = {{WEB_USER}}
listen.group = {{WEB_GROUP}}
listen.mode = 0660
pm = dynamic
pm.max_children = 5
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3
php_admin_value[memory_limit] = 256M
php_admin_value[upload_max_filesize] = 50M
