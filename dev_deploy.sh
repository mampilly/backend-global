#!/bin/bash

# Load the latest container image from tar
docker load < dev_global_api_image.tar

# Operations
file="dev_global_api_tag_old"
if [ -f "$file" ]
then
    # docker service rm Traice-toffline
    # sleep 15
    tag_server=$(cat dev_global_api_tag)
    docker service update traice-global-api --image dev_global_api_image:$tag_server
    tag_server=$(cat dev_global_api_tag_old)
    rm dev_global_api_tag_old
    mv dev_global_api_tag dev_global_api_tag_old
    sleep 15
    docker rmi -f dev_global_api_image:old
    docker tag dev_global_api_image:$tag_server dev_global_api_image:old
    docker rmi -f dev_global_api_image:$tag_server
    tag_server=$(cat dev_global_api_tag_old)
    # Clean images
    docker rm $(docker ps -a -q)
    docker rmi $(docker images -a|grep "<none>"|awk '$1=="<none>" {print $3}') || { echo "no images to remove" ;}
else    
    tag_server=$(cat dev_global_api_tag)
    mv dev_global_api_tag dev_global_api_tag_old
    docker tag dev_global_api_image:$tag_server dev_global_api_image:old
    # Start new service with new image
    docker service create --name traice-global-api -p 80:8000 dev_global_api_image:$tag_server
fi    
