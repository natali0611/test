FROM golang:alpine AS builder
WORKDIR /app
COPY go.mod main.go ./
RUN go build -o go_app

FROM alpine
WORKDIR /app
COPY --from=builder /app/go_app .
RUN chmod +x go_app 
EXPOSE 8080
CMD ["./go_app"]
