# go_app
## 1. Создание web приложения на go с проксированием \ 
### Установка golang

```
sudo apt update
sudo apt upgrade
sudo apt install golang
```

 Создание директории для проекта
`mkdir go_app`

 Создаем файл для приложения  [main.go](https://github.com/natali0611/go_app/blob/simple/main.go)

Создаем файл с зависимостями [go.mod](https://github.com/natali0611/go_app/blob/simple/go.mod)
`go mod init go_app`

Запуск приложения в фоновом режиме `go run main.go &`

### Настройка обратного проксирования с nginx

`sudo apt install nginx -y`

Создание файла [nginx.conf](https://github.com/natali0611/go_app/blob/simple/nginx.conf) и располагаем по данному пути /etc/nginx/conf.d/default

Перезапуск сервера для применения настроек `sudo systemctl reload nginx`

## 2. Запуск приложения с использованием докера

### Создание dockerfile с использованием multistage с целью уменьшения размера образа [Dockerfile](https://github.com/natali0611/go_app/blob/simple/Dockerfile)

Файл находится в папке проекта go_app
Собираем образ
`docker build -t hello .`
запускаем контейнер
`docker run -p "8080:8080" hello`

## 3. Сборка и запуск приложения с обратным прокси путем  docker-compose

Создаем файл [docker-compose.yaml](https://github.com/natali0611/go_app/blob/simple/docker-compose.yaml)
Запускаем `docker-compose up`

## 4. В качестве проверки после запуска приложения в браузере http://localhost:8080 выдается страница с Hello, World!
  (Не заходя в браузер можем проверить исполняемость curl http://localhost:8080)
   При подключении обратного проксирования по пути http://localhost:80 так же выводится Hello, Wold!
   






