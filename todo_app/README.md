** To-do service


*** Start in Docker

`docker pull erlit007/todo-service:0.1.0`
`docker run -d -p 8000:80 -v shorturl:/app/data --name todo-service erlit007/todo-service:0.1.0`


*** Start localy
uvicorn main:app --host 0.0.0.0 --port 80