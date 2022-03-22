#!/bin/bash

while getopts e: argument
do 
    case "${argument}" in
        e) environment=${OPTARG};;
    esac
done

if [ $environment = "DEV" ]
then
    echo "Deploying to Dev Server"
    container_name=traice-dev-redis
    container_port=6379
    container_volume=redis-vol
elif [ $environment = "DEMO" ]
then 
    echo "Deploying to Demo Server"
    container_name=traice-demo-redis
    container_port=6379
    container_volume=redis-vol
elif [ $environment = "PROD-TEST" ]
then 
    echo "Deploying to prod-test Server"
    container_name=traice-prod-test-redis
    container_port=6379
    container_volume=redis-vol
else
    echo "No conditions met"
    exit 1
fi

docker service create --name ${container_name} -p ${container_port}:6379 --mount type=volume,source=${container_volume},destination=/data -d redis:6.2.5