# Flask Movie Database

A Movie library Database which allows users to fetch details of a movie as well as create/edit Movie records such as:
- Movie Name
- Director
- Imdb Score
- Popularity
- Genres
## Tested on :
 - Ubuntu 22.04
## Hosted on :
- Aws Ec2 Instance 
## Components Used:
- Python 3.7/3.10
- SQLlite
- Redis
- Gunicorn
- Docker
- RabbitMq 
- Celery
# Api Reference
## User Creation

```
  POST /v1/user
```
#### Under Authorization - Basic Auth
| Parameter       | Type      | Description                |
| :--------       | :-------  | :------------------------- |
| `Username`      | `string`  |  username|
| `Password`      | `string`  |  password|

#### Request Body
| Parameter       | Type      | Description                |
| :--------       | :-------  | :------------------------- |
| `user_type`      | `string`  |  user/admin(for access purpose)               |


## Token Generation

```
  POST /v1/user
```
#### Request Body
| Parameter       | Type      | Description                  |
| :--------       | :-------  | :-------------------------   |
| `username`      | `string`  | username created in (/v1/user) |
| `token_ttl`      | `integer`  | expiry time for token in minutes |


## List Movies
#### Request Body

```
  GET /v1/search
```

| Parameter         | Type      | Description                |
| :--------         | :-------  | :------------------------- |
| `movie_name`      | `string`  | complete movie name |
| `director_name`   | `string`  | movie director's name |
| `rating`          | `integer` | rating from 1-10(eg.7+) |
| `page_size`       | `integer` | number of elements in the json payload 
| `page_number`     | `integer` | page number to be displayed


## Movie Operations
  Token Mandatory for all operations
```
  POST/PUT /v1/movie
```
#### Request Body
| Parameter         | Type       | Description                  |
| :--------         | :-------   | :-------------------------   |
| `name`            | `string`   | complete movie name |
| `director`        |  `string`  | movie director's name |
| `popularity`      | `integer`  | range 1-100 |
| `imdb_score`      | `integer`  | range 1-10 |
| `genres`          | `list`     | eg. ["Fantasy","Action"]|


```
  DELETE /v1/movie
```
#### Request Body
| Parameter         | Type       | Description                  |
| :--------         | :-------   | :-------------------------   |
| `id`              | `integer`    | movie id  |

# Installation

Python dependencies are in requirements.txt file under /flask_app and /celery_app/src.

For installation of components, follow the below given steps:
```
Install Docker:
	https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

Install RabbitMq:
	sudo docker run -itd  --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management

Configuration:
    sudo rabbitmqctl add_user username password

    sudo rabbitmqctl add_vhost sample_host

    sudo rabbitmqctl set_user_tags username administrator

    sudo rabbitmqctl set_permissions -p sample_host username ".*" ".*" ".*"

Clone Project Repo:
	git clone https://github.com/Justinj64/Flask_Movie_Database.git

Install Make:
	sudo apt install make


```

# Usage
For local instance, change environment variables in *src/config/development.json* and set **ENV=development** in Dockerfile.

Initialize both the applications with the following command.

#### Flask
```bash
../../Flask_Movie_Database/ -> make build && make run
```
#### Celery
```
/workspace/project/Flask_Movie_Database/celery_app -> make build && make run
```

# Logs
```
Api logs    : /Flask_Movie_Database/flask_app/info.log.
Worker logs : /Flask_Movie_Database/celery_app/src/worker.log
```

# Tests
Included under /Flask_Movie_Database/flask_app/Tests
```
  pytest -rA 
```