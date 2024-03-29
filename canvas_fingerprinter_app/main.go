package main

import (
	"fmt"
	"path/filepath"

	"net/http"
	"os"
)

const htmlDirPath = "." // path to html files
const tsDirPath = "."   // path to typescript files

// index returns an handler for serving the main page.
func index() func(w http.ResponseWriter, r *http.Request) {
	endpoint := "index.html"
	return func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("received request for index.html\n")

		switch r.Method {
		case "GET":
			http.ServeFile(w, r, filepath.Join(htmlDirPath, endpoint))
		default:
			fmt.Printf("Recieved unexpected request type at endpoint %s: type = %s", endpoint, r.Method)
			w.WriteHeader(http.StatusMethodNotAllowed)
			w.Write([]byte(fmt.Sprintf("endpoint %s does not support request type %s", endpoint, r.Method)))
		}
	}
}

// fpScript returns a handler for serving the fingerprinting script.
func fpScript() func(w http.ResponseWriter, r *http.Request) {
	endpoint := "fingerprinter.js"
	return func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("received request for fingerprinter.js\n")

		switch r.Method {
		case "GET":
			http.ServeFile(w, r, filepath.Join(tsDirPath, endpoint))
		default:
			fmt.Printf("Recieved unexpected request type at endpoint %s: type = %s\n", endpoint, r.Method)
			w.WriteHeader(http.StatusMethodNotAllowed)
			w.Write([]byte(fmt.Sprintf("endpoint %s does not support request type %s", endpoint, r.Method)))
		}
	}
}

func main() {
	// router := mux.NewRouter()
	port, set := os.LookupEnv("ISSECLAB_PORT")
	if !set {
		port = "8100"
	}
	fmt.Printf("Listening on port %s\n", port)

	// add handlers
	http.HandleFunc("/", index())
	http.HandleFunc("/index.html", index())
	http.HandleFunc("/fingerprinter.js", fpScript())

	err := http.ListenAndServe("127.0.0.1:"+port, http.DefaultServeMux)
	if err != nil {
		fmt.Printf("server error: %v\n", err)
	}

	// // Serve typescript files
	// router.PathPrefix("fingerprinter.js").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
	// 	http.ServeFile(w, r, "./fingerprinter.js")
	// })

	// // Serve index (default)
	// router.PathPrefix("/").HandlerFunc(index)

	// // start http server with given address and a handler
	// err := http.ListenAndServe(":"+port, router)
	// if err != nil {
	// 	log.Fatal("ListenAndServe: ", err)
	// }
}
