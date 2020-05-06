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
      |     requirements.txt
      |     scrapyd.conf
      +---soccer_stats
            ...
```

Add `.env` file to projects `docker` directory and fill it with following variables:
```
POSTGRES_USER=username  # username that should interact with database
POSTGRES_PASSWORD=password  # password for this username
POSTGRES_DB=soccer  # name of database, you can enter here any prefferd name
```
Add `proxy` variables in `.env` file to avoid from blocking (it is not neccesary but recommended):
```
PROXY_URL=proxy_url  # proxy url that should be used in custom proxy middleware for each request
PROXY_USERNAME=proxy_username  # proxy username for authentication purposes (you should get it from proxy provider)
PROXY_PASSWORD=proxy_password  # proxy password for authentication purposes (you should get it from proxy provider)
```

After creating `.env` file execute following command in term:
```
$ docker-compose up -d
```

At this moment scrapyd service and postgres containers should running on your machine.
Change directory to internal `soccer_stats/eggs/` folder and execute request to scrapyd service without `proxy`:
```
curl http://localhost:6800/addversion.json -F project=soccer_stats -F version=0.1 -F egg=@soccer_stats.egg
```
or with `proxy`
```
curl http://localhost:6800/addversion.json -F project=soccer_stats -F version=0.1 -F egg=@soccer_stats_proxy.egg
```
Response from request above:
```
{"node_name": "some_hash", "status": "ok", "project": "soccer_stats", "version": "0.1", "spiders": 1}
```
This mean that you 'load' your project to scrapyd service and now you can push it to do some useful job for you.

Enter command to start crawling:
```
curl http://localhost:6800/schedule.json -F project=soccer_stats -F spider=get_soccer_data
```

Check that job is running:
```
curl http://localhost:6800/listjobs.json?project=soccer_stats
```

Response:
```python
{
    "finished": [],
    "node_name": "some_hash",
    "pending": [],
    "running": [
        {
            "id": "another_some_hash",
            "pid": some_integer,
            "spider": "get_soccer_data",
            "start_time": "some_datetime_value"
        }
    ],
    "status": "ok"
}
```

This mean that spider `get_soccer_data` is running and pulling data to postgres database.

