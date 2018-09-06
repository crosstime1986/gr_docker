#!/usr/bin/env bash
sudo echo "never" > /sys/kernel/mm/transparent_hugepage/enabled
sudo echo "never" >  /sys/kernel/mm/transparent_hugepage/defrag

cat >>/etc/security/limits.conf<<eof
* soft nproc 65535
* hard nproc 65535
* soft nofile 65535
* hard nofile 65535
eof
