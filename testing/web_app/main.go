package main

import (
	"context"
	"encoding/csv"
	"fmt"
	"time"

	"html/template"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

// Testing Link (on campus): http://10.64.57.115:9000/index.html
// Testing LInk (off campus): http://192.168.1.128:9000/index.html

/*
	func IP2Addr(ipAddress string) (result string) {
		IPToAddress, err := gobaidumap.GetAddressViaIP(ipAddress)
		if err != nil {
			fmt.Println(err)
		} else {
			//println(From ip to address - address, IPtoAddress.Content.Address)
			//		fmt.Println("从ip到地址-地址", IPToAddress.Content.Address)
			result = IPToAddress.Content.Address
		}
		return
	}
*/

func WriteFile(content []string, name string, FileServer string) {
	fmt.Printf("File name: %s\n", name)
	f, err := os.OpenFile(".\\"+FileServer+"\\"+name+".xls", os.O_APPEND|os.O_CREATE, os.ModeAppend)
	if err != nil {
		log.Fatal("WriteFile: ", err)
	}
	defer f.Close()

	f.WriteString("\xEF\xBB\xBF")
	writer := csv.NewWriter(f)

	writer.Write(content)

	writer.Flush()
}

func timer(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/timer.html")
		fmt.Println("timer GET")
		log.Println(t.Execute(w, nil))
	}
}

func navigator(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/navigator.html")
		fmt.Println("navigator GET")
		log.Println(t.Execute(w, nil))
	}
}

/*
func iframe(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/iframe.html")
		fmt.Println("iframe GET")
		log.Println(t.Execute(w, nil))
	}
}

func picassauth(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/picassauth.html")
		fmt.Println("picassauth GET")
		log.Println(t.Execute(w, nil))
	}
}
*/

func stanford(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/stanford.html")
		fmt.Println("stanford GET")
		log.Println(t.Execute(w, nil))
	}
}

func oregonState(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/oregonState.html")
		fmt.Println("oregonState GET")
		log.Println(t.Execute(w, nil))
	}
}

func auburn(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/auburn.html")
		fmt.Println("auburn GET")
		log.Println(t.Execute(w, nil))
	}
}

func alaska(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/alaska.html")
		fmt.Println("alaska GET")
		log.Println(t.Execute(w, nil))
	}
}

func texas(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/texas.html")
		fmt.Println("texas GET")
		log.Println(t.Execute(w, nil))
	}
}

func pennState(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/pennState.html")
		fmt.Println("pennState GET")
		log.Println(t.Execute(w, nil))
	}
}

func northDakota(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/northDakota.html")
		fmt.Println("northDakota GET")
		log.Println(t.Execute(w, nil))
	}
}

func colorado(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/colorado.html")
		fmt.Println("colorado GET")
		log.Println(t.Execute(w, nil))
	}
}

/*
	func dartmouth(w http.ResponseWriter, r *http.Request) {
		if r.Method == "GET" {
			t, _ := template.ParseFiles("./html/dartmouth.html")
			fmt.Println("dartmouth GET")
			log.Println(t.Execute(w, nil))
		}
	}
*/

func maine(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/maine.html")
		fmt.Println("maine GET")
		log.Println(t.Execute(w, nil))
	}
}

func wisconsin(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/wisconsin.html")
		fmt.Println("wisconsin GET")
		log.Println(t.Execute(w, nil))
	}
}

func florida(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/florida.html")
		fmt.Println("florida GET")
		log.Println(t.Execute(w, nil))
	}
}

func cssGet(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./static/html/bootstrap.min.css")
		fmt.Println("Css GET")
		log.Println(t.Execute(w, nil))
	}
}

func index(w http.ResponseWriter, r *http.Request) {
	// client accessing index.html...
	if r.Method == "GET" {
		http.ServeFile(w, r, "./static/html/index.html")
	}
	// client sending link-state information...
	if r.Method == "POST" {
		// Call ParseForm() to parse the raw query and update r.PostForm and r.Form.
		if err := r.ParseForm(); err != nil {
			fmt.Fprintf(w, "ParseForm() err: %v", err)
			return
		}

		client, err := mongo.NewClient(options.Client().ApplyURI("mongodb+srv://joslinn1:3Dd4AdJq7briU3TV@pinglocdata.dsgop.mongodb.net/?retryWrites=true&w=majority"))
		if err != nil {
			log.Fatal(err)
		}
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		err = client.Connect(ctx)
		if err != nil {
			log.Fatal(err)
		}
		defer client.Disconnect(ctx)
		err = client.Ping(ctx, readpref.Primary())
		if err != nil {
			log.Fatal(err)
		}
		/*
			databases, err := client.ListDatabaseNames(ctx, bson.M{})
			if err != nil {
				log.Fatal(err)
			}
			fmt.Println("Retreived Databases: ", databases)
		*/
		pingLocDatabase := client.Database("PingLocDatabase")
		userLinkStateCollection := pingLocDatabase.Collection("UserLinkStateInformation")

		var userData interface{}
		userDataJSON := r.FormValue("userData")
		err = bson.UnmarshalExtJSON([]byte(userDataJSON), true, &userData)
		if err != nil {
			// log.Fatal(err)	// we don't want the server crashing on errors...
			fmt.Println("[ERROR] Unable to unmarshal user data...")
		}

		// fmt.Println("Received User Data: ", userData)

		// insert the data to the database
		_, err = userLinkStateCollection.InsertOne(ctx, userData)
		if err != nil {
			// log.Fatal(err)	// we don't want the server crashing on errors...
			fmt.Println("[ERROR] Unable to insert user data to database...")
		}
		fmt.Println("Successfully stored link-state information for a user!")
	}
}

// var userLinkStateCollection *mongo.Collection // must be global if we don't want to connect->disconnect every write
// var ctx context.Context
// var client *mongo.Client

func main() {
	fmt.Println("Starting up...")

	router := mux.NewRouter()
	port := os.Getenv("PORT")

	// Serve javascript files
	router.PathPrefix("/js/ping.js").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/js/ping.js")
	})
	router.PathPrefix("/js/graph.js").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/js/graph.js")
	})

	// Serve css file
	router.PathPrefix("/bootstrap.min.css").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/bootstrap.min.css")
	})

	// Serve html files
	router.PathPrefix("/timer.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/timer.html")
	})
	router.PathPrefix("/stanford.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/stanford.html")
	})
	router.PathPrefix("/oregonState.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/oregonState.html")
	})
	router.PathPrefix("/auburn.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/auburn.html")
	})
	router.PathPrefix("/alaska.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/alaska.html")
	})
	router.PathPrefix("/texas.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/texas.html")
	})
	router.PathPrefix("/pennState.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/pennState.html")
	})
	router.PathPrefix("/northDakota.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/northDakota.html")
	})
	router.PathPrefix("/colorado.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/colorado.html")
	})
	router.PathPrefix("/maine.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/maine.html")
	})
	router.PathPrefix("/wisconsin.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/wisconsin.html")
	})
	router.PathPrefix("/florida.html").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/html/florida.html")
	})

	// Serve index (default)
	router.PathPrefix("/").HandlerFunc(index)

	// start http server with given address and a handler
	err := http.ListenAndServe(":"+port, router)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
