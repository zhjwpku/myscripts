#!/bin/bash
if [ -z $1 ]; then
  yesterday=`date -d "yesterday" +"%Y-%m-%d"`
else
  yesterday=$1
fi
save_days=7

echo "orange-api-gateway-access-${yesterday}.log.gz"

scp -i /root/.ssh/keys/appvideo_ir ec2-user@54.246.180.162:/opt/startimes/log/orange-api-gateway-access/orange-api-gateway-access-${yesterday}.log.gz .

gzip -d orange-api-gateway-access-${yesterday}.log.gz

find . -mtime +$save_days -exec rm -rf {} \;


