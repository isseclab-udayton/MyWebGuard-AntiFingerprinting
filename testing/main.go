package main

import (
	"encoding/csv"
	"fmt"

	// "gobaidumap"
	"html/template"
	"log"
	"net/http"
	"os"
	"strings"
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
		t, _ := template.ParseFiles("./html/bootstrap.min.css")
		fmt.Println("Css GET")
		log.Println(t.Execute(w, nil))
	}
}

func index(w http.ResponseWriter, r *http.Request) {
	// client attempting to access index.html...
	if r.Method == "GET" {
		t, _ := template.ParseFiles("./html/index.html")
		fmt.Println("index GET")
		log.Println(t.Execute(w, nil))
	}
	// client attempting to send information...
	// this is where data is collected?
	if r.Method == "POST" {
		fmt.Println("index POST")
		//Get user IP
		loginip := strings.Split(r.RemoteAddr, ":")[0]
		fmt.Println("ip:", loginip)
		// IP2Addr(loginip)		supposed to return a string, but return value is not used so whats the point?
		//processing form
		// Addr := r.ParseForm()	// OG PingLoc code, it returns an error so not sure what they're doing here...
		// fmt.Println("Addr:", Addr)

		// Nathan's updated version...
		err := r.ParseForm()
		if err != nil {
			panic(err)
		}
		fmt.Println("name:", r.Form["name2"])

		// servers
		fmt.Println("Stanford:", r.Form["StanfordVal"])
		fmt.Println("Oregon State:", r.Form["Oregon StateVal"])
		fmt.Println("Auburn:", r.Form["AuburnVal"])
		fmt.Println("Alaska:", r.Form["AlaskaVal"])
		fmt.Println("Texas:", r.Form["TexasVal"])
		fmt.Println("Penn State:", r.Form["Penn StateVal"])
		fmt.Println("North Dakota:", r.Form["North DakotaVal"])
		fmt.Println("Colorado:", r.Form["ColoradoVal"])
		fmt.Println("Maine:", r.Form["MaineVal"])
		fmt.Println("Wisconsin:", r.Form["WisconsinVal"])
		fmt.Println("Florida:", r.Form["FloridaVal"])

		/*
			// navigator
			fmt.Println("deviceType:", r.Form["deviceType"])
			fmt.Println("OSname:", r.Form["OSname"])
			fmt.Println("browserName:", r.Form["browserName"])
			fmt.Println("browserVer:", r.Form["browserVer"])
			fmt.Println("adaptType:", r.Form["adaptType"])
		*/

		// write the data
		// WriteFile(content []string,name string,FileServer string)
		// NOTE: Removed "r.Form["dartmouth"][0],"
		//data := []string{"", r.Form["stanford"][0], r.Form["oregonState"][0], r.Form["auburn"][0], r.Form["alaska"][0], r.Form["texas"][0], r.Form["pennState"][0], r.Form["northDakota"][0], r.Form["colorado"][0], r.Form["wisconsin"][0], r.Form["florida"][0]}
		//WriteFile(data, r.Form["name"][0], "hash")
		/*
			data2 := []string{r.Form["name"][0], loginip, r.Form["deviceType"][0], r.Form["OSname"][0], r.Form["browserName"][0], r.Form["browserVer"][0], r.Form["adaptType"][0]}
			WriteFile(data2, r.Form["name"][0], "ip")
		*/
	}
}

func main() {
	fmt.Println("connecting 127.0.0.1:9000 ......")
	fs := http.FileServer(http.Dir("js"))
	http.Handle("/js/", http.StripPrefix("/js/", fs))

	// when these paths are requested, call this function to do stuff...
	http.HandleFunc("/", index)
	http.HandleFunc("/bootstrap.min.css", cssGet)
	http.HandleFunc("/timer.html", timer)
	http.HandleFunc("/navigator.html", navigator)
	// http.HandleFunc("/picassauth.html", picassauth)
	// http.HandleFunc("/iframe.html", iframe)
	http.HandleFunc("/stanford.html", stanford)
	http.HandleFunc("/oregonState.html", oregonState)
	http.HandleFunc("/auburn.html", auburn)
	http.HandleFunc("/alaska.html", alaska)
	http.HandleFunc("/texas.html", texas)
	http.HandleFunc("/pennState.html", pennState)
	http.HandleFunc("/northDakota.html", northDakota)
	http.HandleFunc("/colorado.html", colorado)
	// http.HandleFunc("/dartmouth.html", dartmouth)
	http.HandleFunc("/maine.html", maine)
	http.HandleFunc("/wisconsin.html", wisconsin)
	http.HandleFunc("/florida.html", florida)

	// start http server with given address and a handler. handler is usually nil, which
	// means to use DefaultServeMux
	// Handle and HandleFunc add handlers to DefaultServeMux
	err := http.ListenAndServe(":9000", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
