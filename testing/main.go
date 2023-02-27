package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"encoding/csv"
	"strings"
	"gobaidumap"
)

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


func WriteFile(content []string,name string,FileServer string) {
	f, err := os.OpenFile("./"+FileServer+"/"+name+".xls", os.O_APPEND|os.O_CREATE, os.ModeAppend)
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
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/timer.html")
		fmt.Println("timer GET")
		log.Println(t.Execute(w, nil))
	}
}

func navigator(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/navigator.html")
		fmt.Println("navigator GET")
		log.Println(t.Execute(w, nil))
	}
}

func iframe(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/iframe.html")
		fmt.Println("iframe GET")
		log.Println(t.Execute(w, nil))
	}
}

func picassauth(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/picassauth.html")
		fmt.Println("picassauth GET")
		log.Println(t.Execute(w, nil))
	}
}

func baidu(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/baidu.html")
		fmt.Println("baidu GET")
		log.Println(t.Execute(w, nil))
	}
}

func sina(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/sina.html")
		fmt.Println("sina GET")
		log.Println(t.Execute(w, nil))
	}
}

func nju(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/nju.html")
		fmt.Println("nju GET")
		log.Println(t.Execute(w, nil))
	}
}

func iqiyi(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/iqiyi.html")
		fmt.Println("iqiyi GET")
		log.Println(t.Execute(w, nil))
	}
}

func douban(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/douban.html")
		fmt.Println("douban GET")
		log.Println(t.Execute(w, nil))
	}
}

func so(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/so.html")
		fmt.Println("so GET")
		log.Println(t.Execute(w, nil))
	}
}

func youku(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/youku.html")
		fmt.Println("youku GET")
		log.Println(t.Execute(w, nil))
	}
}

func qidian(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/qidian.html")
		fmt.Println("qidian GET")
		log.Println(t.Execute(w, nil))
	}
}

func ersansiwu(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/2345.html")
		fmt.Println("2345 GET")
		log.Println(t.Execute(w, nil))
	}
}

func dianping(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/dianping.html")
		fmt.Println("dianping GET")
		log.Println(t.Execute(w, nil))
	}
}

func seu(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/seu.html")
		fmt.Println("seu GET")
		log.Println(t.Execute(w, nil))
	}
}

func index(w http.ResponseWriter, r *http.Request) {
	if r.Method =="GET" {
		t, _ := template.ParseFiles("./html/index.html")
		fmt.Println("index GET")
		log.Println(t.Execute(w, nil))
	}
	if r.Method =="POST" {
		fmt.Println("index POST")
		//Get user IP
		loginip := strings.Split(r.RemoteAddr, ":")[0]
		fmt.Println("ip:",loginip)
		IP2Addr(loginip);
		//processing form
		Addr := r.ParseForm()
		fmt.Println("Addr:",Addr)
		fmt.Println("name:",r.Form["name"])
		fmt.Println("baidu:",r.Form["baidu"])
		fmt.Println("sina:",r.Form["sina"])
		fmt.Println("nju:",r.Form["nju"])
		fmt.Println("iqiyi:",r.Form["iqiyi"])
		fmt.Println("douban:",r.Form["douban"])
		fmt.Println("so:",r.Form["so"])
		fmt.Println("youku:",r.Form["youku"])
		fmt.Println("qidian:",r.Form["qidian"])
		fmt.Println("2345:",r.Form["2345"])
		fmt.Println("dianping:",r.Form["dianping"])
		fmt.Println("seu:",r.Form["seu"])
		fmt.Println("deviceType:",r.Form["deviceType"])
		fmt.Println("OSname:",r.Form["OSname"])
		fmt.Println("browserName:",r.Form["browserName"])
		fmt.Println("browserVer:",r.Form["browserVer"])
		fmt.Println("adaptType:",r.Form["adaptType"])
		data := []string{"",r.Form["baidu"][0],r.Form["sina"][0],r.Form["nju"][0],r.Form["iqiyi"][0],r.Form["douban"][0],r.Form["so"][0],r.Form["youku"][0],r.Form["qidian"][0],r.Form["2345"][0],r.Form["dianping"][0],r.Form["seu"][0]}
		WriteFile(data,r.Form["name"][0],"hash")
		data2 := []string{r.Form["name"][0],loginip,r.Form["deviceType"][0],r.Form["OSname"][0],r.Form["browserName"][0],r.Form["browserVer"][0],r.Form["adaptType"][0]}
		WriteFile(data2,r.Form["name"][0],"ip")
	}
}


func main() {
	// connecting 127.0.0.1:9000 .......
	fmt.Println("正在连接127.0.0.1:9000 ......")
	fs := http.FileServer(http.Dir("js"))
	http.Handle("/js/", http.StripPrefix("/js/", fs))

	// when these paths are requested, call this function to do stuff...
	http.HandleFunc("/",index)
	http.HandleFunc("/timer.html",timer)
	http.HandleFunc("/navigator.html",navigator)
	http.HandleFunc("/picassauth.html",picassauth)
	http.HandleFunc("/iframe.html",iframe)
	http.HandleFunc("/baidu.html",baidu)
	http.HandleFunc("/sina.html",sina)
	http.HandleFunc("/nju.html",nju)
	http.HandleFunc("/iqiyi.html",iqiyi)
	http.HandleFunc("/douban.html",douban)
	http.HandleFunc("/so.html",so)
	http.HandleFunc("/youku.html",youku)
	http.HandleFunc("/qidian.html",qidian)
	http.HandleFunc("/2345.html",ersansiwu)
	http.HandleFunc("/dianping.html",dianping)
	http.HandleFunc("/seu.html",seu)

	// start http server with given address and a handler. handler is usually nil, which
	// means to use DefaultServeMux
	// Handle and HandleFunc add handlers to DefaultServeMux
	err := http.ListenAndServe(":9000", nil)
	if err != nil {
	log.Fatal("ListenAndServe: ", err)
	}
}

