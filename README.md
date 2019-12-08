# soccer-stats
Project to fetch soccer data from web

#### How to start
Clone repository
```
$ git clone https://github.com/ESm1th/soccer-stats.git
```

Install docker and docker-compose on your OS. For example url to **Ubuntu Linux** installation guide - https://docs.docker.com/install/linux/docker-ce/ubuntu/

Structure
```
+---soccer_stats
      |   .gitignore
      |   README.md
      |---docker
      |     .env
      |     docker-compose.yml
      |     Dockerfile
      |     mongo-init.sh
      |     requirements.txt
      |     scrapyd.conf
      +---soccer_stats
            ...
```

Add `.env` file to projects `docker` directory and fill it with following variables:
```
MONGO_USERNAME=username  # username that should interact with database
MONGO_PASSWORD=password  # password for this username
MONGO_DATABASE=soccer  # name of database, you can enter here any prefferd name
MONGO_LEAGUES_COLLECTION=leagues  # collection name for fetched leagues
MONGO_MATCHES_COLLECTION=matches  # collection name for fetched matches
```

After creating `.env` file execute following command in term:
```
$ docker-compose up -d
```

At this moment scrapyd service and mongodb containers should running on your machine.
Change directory to internal soccer_stats folder and execute request to scrapyd service:
```
curl http://localhost:6800/addversion.json -F project=soccer_stats -F version=0.1 -F egg=@soccer_stats.egg
```
Response from request above:
```
{"node_name": "some_hash", "status": "ok", "project": "soccer_stats", "version": "0.1", "spiders": 1}
```
This mean that you 'load' your project to scrapyd service and now you can push it to do some useful job for you.


