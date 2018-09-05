# gr_docker

-----------------------------

```

```




```
docker run -d -v /data/www:/home/www --name php712 crosstime1986/php:7.1.2-fpm

docker run -d -p 80:80  --link php712:php712 -v /data/etc/nginx/conf.d:/etc/nginx/conf.d --volumes-from php712  --name nginx  nginx:1.14.0-alpine

```