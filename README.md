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
      |   .env
      |   .gitignore
      |   README.md
      |   requirements.txt
      |---docker
      |     docker-compose.yml
      |     Dockerfile
      |     mongo-init.sh
      |     scrapyd.conf
      +---soccer_stats
          ...
```
Add `.env` file to projects `root` directory and fill it with following variables:
```
MONGO_USERNAME=username  # username that should interact with database
MONGO_PASSWORD=password  # password for this username
MONGO_URI=mongodb://username:password@localhost/admin  # username and password from previous variables
MONGO_DATABASE=soccer  # name of database, you can enter here any prefferd name
MONGO_LEAGUES_COLLECTION=leagues  # collection name for fetched leagues
MONGO_MATCHES_COLLECTION=matches  # collection name for fetched matches
```

Change directory to projects `docker` folder (where are located `Dockerfile` and `docker-compose.yml`).
Execute following commands in term:
```
$ docker-compose up -d
```

Change directory to project `root` folder, create virtual environment and activate it with following command:
```
$ mkvirtualenv soccer --python=python3
```

And after virtual environment created:
```
$ pip install -r requirements.txt
```

Then change directory to internal `soccer_stats` folder and execute crawling command:
```
$ scrapy crawl get_soccer_stats
```
