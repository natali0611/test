# go_app
## 1. Создание web приложения на go с проксированием  
### Установка golang

```
sudo apt update
sudo apt upgrade
sudo apt install golang
```

 Создание директории для проекта
`mkdir go_app`

 Создаем файл для приложения  [main.go](https://github.com/natali0611/go_app/blob/simple/main.go)
```
package main

import (
	"fmt"
        "net/http"
)

func hello(w http.ResponseWriter, r *http.Request) { 
    fmt.Fprint(w, "Hello, World!")
}

func main() {            # 
	http.HandleFunc("/", hello)
        fmt.Println("Listening on port 8080    ") 
        http.ListenAndServe(":8080", nil)
}
```
Создаем файл с зависимостями [go.mod](https://github.com/natali0611/go_app/blob/simple/go.mod)
`go mod init go_app`

Запуск приложения в фоновом режиме `go run main.go &`

### Настройка обратного проксирования с nginx

`sudo apt install nginx -y`

Создание файла [nginx.conf](https://github.com/natali0611/go_app/blob/simple/nginx.conf) и располагаем по данному пути /etc/nginx/conf.d/default
```
server {
    listen 80;             
    server_name localhost;
    
    location / {
        proxy_pass http://go_app:8080; 
        proxy_set_header Host $host;
        proxy_set_header X-Real_IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Перезапуск сервера для применения настроек `sudo systemctl reload nginx`

## 2. Запуск приложения с использованием docker

### Создание dockerfile с использованием multistage с целью уменьшения размера образа [Dockerfile](https://github.com/natali0611/go_app/blob/simple/Dockerfile)
```
FROM golang:alpine AS builder #Для компиляции приложения
WORKDIR /app
COPY go.mod main.go ./
RUN go build -o go_app

FROM alpine #Запуск уже скомпилированного приложения
WORKDIR /app
COPY --from=builder /app/go_app .
RUN chmod +x go_app 
EXPOSE 8080
CMD ["./go_app"]
```
Файл находится в папке проекта go_app
Собираем образ
`docker build -t hello .`
запускаем контейнер
`docker run -p "8080:8080" hello`

## 3. Сборка и запуск приложения с обратным прокси путем  docker-compose

Создаем файл [docker-compose.yaml](https://github.com/natali0611/go_app/blob/simple/docker-compose.yaml)
Запускаем `docker-compose up`
```
services:
  go_app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - go_app
```

## 4. В качестве проверки после запуска приложения в браузере http://localhost:8080 выдается страница с Hello, World!
  (Не заходя в браузер можем проверить исполняемость curl http://localhost:8080)
   При подключении обратного проксирования по пути http://localhost:80 так же выводится Hello, Wold!
 






