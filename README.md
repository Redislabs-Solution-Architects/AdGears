## Running with Docker

### Prerequisites 
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running Dockerized Version

```
git clone https://github.com/maguec/redisearch_demo_and_preso
cd redisearch_demo_and_preso
docker-compose up
```

[Open This Link in Your Browser](http://localhost:5000)


## Running Locally

### Starup docker container

```
docker run --rm -p 6379:6379 redislabs/redismod:latest
```

### Install python requirements

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Start the flask app

```
python3 app.py 
```

### Navigate to the home page

1) [Webapp](http://localhost:5000)

2) Data will automatically load if the key is not already present

3) Start typing in the text box

### Redis Insight

Redis Insight is [running](http://localhost:8001) as well

### Running manually

Getting ad per user:

```
RG.TRIGGER adserv "Ha Ji-Won"
```

Adding a new campaign

```
ZADD campaign:Female:100-200K:30-35 20 "Super Premium Bags"
SET counter:SuperPremiumBags 100
```
