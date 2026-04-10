docker build -t how-to-agent .

docker stop how-to-agent
docker rm how-to-agent

docker run -d -p 3978:3978 --env-file .env --name how-to-agent how-to-agent
docker logs -f how-to-agent