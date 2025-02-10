# Создание приложения на Go, которое отображает в браузере "Hello, World!"
## Предварительные требования:
* Ubuntu 22.04 or lower
* Installed golang
* Docker
* Docker-compose

##  Создание web приложения на go   

 Создание директории для проекта
```
mkdir go_app
```

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

func main() {             
	http.HandleFunc("/", hello)
        fmt.Println("Listening on port 8080    ") 
        http.ListenAndServe(":8080", nil)
}
```
Создаем файл с зависимостями [go.mod](https://github.com/natali0611/go_app/blob/simple/go.mod)
```
go mod init go_app
```

Запуск приложения в фоновом режиме
```
go run main.go &
```
Проверка запущенного приложения
```
curl http://localhost:8080
```
##  Запуск приложения с использованием docker

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
```
docker build -t hello .
```
запускаем контейнер
```
docker run -p "8080:8080" hello
```

## Сборка и запуск приложения с обратным прокси путем  docker-compose

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

Проверяем  в браузере http://localhost:80 отображается страница "Hello, World!"
 






