# soccer-stats
Project to fetch soccer data from web

#### How to start
Clone repository
```
$ git clone https://github.com/ESm1th/soccer-stats.git
```

Install docker and docker-compose on your OS. For example url to **Ubuntu Linux** installation guide - https://docs.docker.com/install/linux/docker-ce/ubuntu/

Add `.env` file to projects `root` directory and fill it with following variables:
```
MONGO_USERNAME=username  # username that should interact with database
MONGO_PASSWORD=password  # password for this username
MONGO_URI=mongodb://username:password@localhost/admin  # username and password from previous variables
MONGO_DATABASE=soccer  # name of database, you can enter here any prefferd name
MONGO_LEAGUES_COLLECTION=leagues  # collection name for fetched leagues
MONGO_MATCHES_COLLECTION=matches  # collection name for fetched matches
```
Change directory to projects `root` folder (where are located `Dockerfile` and `docker-compose.yml`).
```
+---soccer_stats
      |   .env
      |   .gitignore
      |   docker-compose.yml
      |   Dockerfile
      |   mongo-init.sh
      |   requirements.txt
      |   scrapyd.conf
      +---soccer_stats
```
Execute following commands in term:

```
$ docker-compose up -d
```
Create virtual environment and activate it:
```
$ mkvirtualenv soccer --python=python3
```
And after virtual environment created:
```
$ pip install -r requirements.txt
```
Then change directory to internal `soccer_stats` folder and execute crawling command:
```
$ scrapy crawl footy_stats_spider
```
