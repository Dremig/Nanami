docker rm -f nanami # you can comment this line if you don't want to remove the old container
docker build -t nanami .
docker run --name nanami -p 5000:5000 nanami