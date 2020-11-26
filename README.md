## Running with Docker

### Description
This application is built to demonstrate how to:

  - Minimize latency for serving real time ads
  - Maximizing the revenue generated per impression
  - Illustrate the ability to de-duplicate impressions
  - Show how to use event based statistics in time series

Utilizing:

- [RedisGears](https://redisgears.io) for customization and optimization
- [RedisBloom](https://redisbloom.io) for de-duplication
- [RedisTimeseries](https://redistimeseries.io) for event statistics
- [Redis Streams](https://redis.io/topics/streams-intro) for event queuing
- [Python Flask](https://palletsprojects.com/p/flask/) to serve the Web UI
- [Chart.js](https://www.chartjs.org/) to display data

Goals:

  - Simple, easy to understand code
  - Detail key points in serving and customizing ads


### Prerequisites 
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running Dockerized Version

```
git clone https://github.com/Redislabs-Solution-Architects/AdGears.git
cd AdGears
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

2) Data will automatically load  if it is not already present

3) Start askign for ads

### Redis Insight

Redis Insight is [running](http://localhost:8001) as well

