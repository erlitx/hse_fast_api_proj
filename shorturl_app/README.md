*** Short URL service

*** Start in Docker

`docker pull erlit007/shorturl-service:0.1.0`
`docker run -d -p 8001:80 -v shorturl:/app/data --name shorturl-service erlit007/shorturl-service:0.1.0`


*** Start localy
uvicorn main:app --host 0.0.0.0 --port 80
