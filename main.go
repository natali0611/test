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

