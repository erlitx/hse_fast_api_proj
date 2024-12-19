## To-do service

Находится в `todo_app`

### Start in Docker

`docker pull erlit007/todo-service:0.1.0`

`docker run -d -p 8000:80 -v todo_data:/app/data --name todo-service erlit007/todo-service:0.1.0`


### Start localy

`uvicorn main:app --host 0.0.0.0 --port 80`

-----------------------------------------------

## Short URL service

Находится в `shorturl_app`

### Start in Docker

`docker pull erlit007/shorturl-service:0.1.0`

`docker run -d -p 8001:80 -v shorturl_data:/app/data --name shorturl-service erlit007/shorturl-service:0.1.0`


### Start localy
`uvicorn main:app --host 0.0.0.0 --port 80`
