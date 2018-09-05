FROM helder/php-5.3

RUN  apt-get update \
  && apt-get install -y libfreetype6-dev libjpeg-dev libpng-dev \
  && mkdir -p /usr/include/freetype2/freetype/ \
  && ln -s /usr/include/freetype2/freetype.h /usr/include/freetype2/freetype/freetype.h \
  && docker-php-ext-configure gd --enable-gd-native-ttf --with-jpeg-dir=/usr/lib/x86_64-linux-gnu --with-png-dir=/usr/lib/x86_64-linux-gnu --with-freetype-dir=/usr/lib/x86_64-linux-gnu \
  && docker-php-ext-install gd \
  && docker-php-ext-install mbstring \
  && pecl install xdebug-2.2.0 \
  && pecl install redis-2.2.7 \
  && apt-get -y install libgearman-dev \
  && pecl install gearman \
  && pecl install memcache \
  && apt-get -y install libmemcached-dev build-essential \
  && pecl install memcached --with-libmemcached-dir \
  && cd /usr/src/php \
  && rm -rf /var/lib/apt/lists/* \
  && make clean


COPY php.ini-production /usr/local/etc/php/php.ini

EXPOSE 9000