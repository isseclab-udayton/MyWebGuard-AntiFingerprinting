// A COPY FROM PINGLOC NOT ORIGINAL CODE
// [Paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9500556)
// [Github](https://github.com/1362860831/PingLoc)

//NATHAN: It appears that CORS is only enforced on images if they are drawn to
//        canvas using drawImage(). Source: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

function ping(ip,id){
    var img = new Image();								//Although it is an Image object here, we are actually building a cache. Of course, you can also pretend that you just want to obtain the resources of a third-party website, so as to cover up your real purpose
    var start = 0;										//start time
    var end = 0;										//stop the time
    var flag = false;									//Flag bit, confirm whether to complete the cache
    var isCloseWifi = true;								//flag, confirm network status
    var hasFinish = false;								//Flag bit, confirm whether the ping work has ended

    var MAX_LIMIT = 800;
    var time = MAX_LIMIT;									//The result of ping, the initial value is set to a very large result, which is convenient for subsequent processing

    img.onload = function() {							//Here are the tasks to be performed when creating the cache, but our purpose is not here! ! !
        if ( !hasFinish ) {
            flag = true;								//Modify the flag, we have obtained the cache
            hasFinish = true;							//Modify the flag bit, our ping work has been completed
//            console.log('ONLOAD!!!');	//output some log information
        }
    };
    img.onerror = function() {							//Here is the part where the exception jumps out, because we didn't cache the picture at all, so we will definitely jump here
        //console.log("Image loading error, as expected...")
        if ( !hasFinish ) {								//if work is not done
            if ( !isCloseWifi ) {						//And the network is smooth, that is, the target website has been found, but this website does not have the resources we need
                flag = true;							//ok~ this is what we want to achieve
                end = new Date().getTime();				//Indicates that we have "pinged"
                time = end - start;
//                console.log('Ping ' + ip + ' success. '+ time);
//                console.log("success to "+ip);
            } else {									//Otherwise, there is a problem with the network
//                console.log('network is not working!');
            }
            hasFinish = true;
        }
    };

    //NATHAN: After 2 ms try again?
    setTimeout(function(){									//Website resources are sometimes unavailable, set a timeout
        isCloseWifi = false;								//Modify the flag bit, the network is smooth
//        console.log('network is working, start ping...');	//output some log information
//        console.log("I am testing "+ip);							//pop-up notice
    },2);

    //NATHAN: This is really where ping beings...
    start = new Date().getTime();									//start the timer
    img.src = 'http://' + ip + '/' + start;					//This is the real goal of establishing the target website cache. The purpose of adding a small tail here is to make him jump out abnormally!
    console.log("Pinging " + img.src + " ...");

	setTimeout(function(){									//Here we write the time we have counted into the form
		//document.getElementById(id).value = time            //NATHAN: id is the website they are pinging
		console.log("Ping time elapsed: " + time + "--- Src: " + img.src)
        },MAX_LIMIT+1
	);

/*
	var timer = setTimeout(function() {
        if ( !flag ) {										//If no cache is created
            hasFinish = true;								//Close the handler entry of onload and onerror
            flag = false ;
            console.log('Ping ' + ip + ' fail. ');			//output log
        }
    }, MAX_LIMIT);
*/
}