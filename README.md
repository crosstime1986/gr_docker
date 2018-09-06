# 公司生产和线上用的容器环境

-----------------------------



## nginx 虚拟主机配置 

```
server
{
        listen       80;
        server_name  chat.gaore.com;
        root   /home/www/chat.gaore.com/public;
        index index.php index.html;
        charset utf-8;

        try_files $uri $uri/ @rewrite;


        location @rewrite {
            rewrite ^/(.*)$ /index.php?_url=/$1;
        }

        location ~ \.php {
            fastcgi_param PHP_VALUE "xdebug.idekey=CHATGAORE \n xdebug.remote_port=9015";
            fastcgi_pass  php712:9000;
            fastcgi_index index.php;
            fastcgi_param GAORE_ENVIRONMENT 'development';
            fastcgi_param GAORE_DEBUG 'On';
	        include fastcgi.conf;
            fastcgi_split_path_info       ^(.+\.php)(/.+)$;
            fastcgi_param PATH_INFO       $fastcgi_path_info;
            # php.ini 配置也要把 fix_cgi_pathinfo = 0
            # fastcgi_param PATH_TRANSLATED $document_root$fastcgi_path_info;
        }

        location ~ /\.ht {
            deny  all;
        }

        location ~ /\.git {
            deny  all;
        }
}
```

## 启动

```
docker run -d -v /data/www:/home/www --name php712 crosstime1986/php:7.1.2-fpm

docker run -d -p 80:80  --link php712:php712 \
       -v /data/etc/nginx/conf.d:/etc/nginx/conf.d \
       --volumes-from php712  \
       --name nginx  nginx:1.14.0-alpine
```