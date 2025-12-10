server {
    listen 80;
    server_name {{HOSTNAME}};
    root {{DOCUMENT_ROOT}};
    index index.php index.html;

    #access_log {{ACCESS_LOG}};
    #error_log {{ERROR_LOG}};
    access_log /dev/stdout vhost;
    error_log /dev/stderr warn vhost_error;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_pass unix:{{PHP_SOCKET}};
    }
}
