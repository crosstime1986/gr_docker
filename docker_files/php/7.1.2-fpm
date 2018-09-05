FROM php:7.1.21-fpm-alpine3.8

MAINTAINER liangzy@gaore.com

ARG PHALCON_VERSION=3.2.4

ARG PHALCON_EXT_PATH=php7/64bits

RUN set -xe && \
        # Compile Phalcon
        curl -LO https://github.com/phalcon/cphalcon/archive/v${PHALCON_VERSION}.tar.gz && \
        tar xzf ${PWD}/v${PHALCON_VERSION}.tar.gz && \
        docker-php-ext-install -j $(getconf _NPROCESSORS_ONLN) ${PWD}/cphalcon-${PHALCON_VERSION}/build/${PHALCON_EXT_PATH} && \
        # Remove all temp files
        rm -r \
            ${PWD}/v${PHALCON_VERSION}.tar.gz \
            ${PWD}/cphalcon-${PHALCON_VERSION}

RUN set -xe && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add --no-cache --update libmemcached-dev yaml-dev zlib-dev gcc autoconf g++ make libffi-dev openssl-dev && \
    pecl install igbinary  && \
    docker-php-ext-enable igbinary && \
    echo 'yes' | pecl install redis  && \
    docker-php-ext-enable redis && \
    echo 'no' | pecl install memcached  && \
    docker-php-ext-enable memcached && \
    pecl install mongodb-1.5.2  && \
    docker-php-ext-enable mongodb && \
    pecl install yaml  && \
    docker-php-ext-enable yaml && \
    docker-php-ext-install pdo_mysql && \
    rm -rf /tmp/*

EXPOSE 9000