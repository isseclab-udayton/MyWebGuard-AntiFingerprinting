var injectee = document.createElement("script");
injectee.innerHTML = `
(function() {
  var host_origin = (new URL(window.location)).origin;
  var CORS_enabled = 'withCredentials' in new XMLHttpRequest();
  //alert("Debug: host_origin="+host_origin);
  var origin_source_read = new Map();
  var debug = true;
  function mywebguard_log(s){
      if((!debug) || (!console.log)) return;
      console.log('mywebguard log: '+s);
  }
  mywebguard_log("starting mywebguard.js");
  console.log("Edited");
  //store builtin functions to keep their original implementations
  var $Array = Array;
  var $Object = window.Object;
  var hasOwnProperty = Object.prototype.hasOwnProperty;
  var originalDocument_createElelment = document.createElement; //we need to keep the original copy so that our code will not be intercepted.

  var builtins = {};

  builtins.__proto__ = null;
  with (Function.prototype)
    builtins.Function = { apply: apply, call: call, toString: toString };
  try {
    // Create a function from a string.  Note that functions created with
    // the Function constructor DO NOT get a scope chain that includes the
    // current lexical scope; their scope chains include only the global
    // context.  To export local function declarations, we do some simple
    // parsing of the string form of the function and append commands that
    // explicitly export each definition.  Ads can obviously defeat this
    // eaprocess in a variety of ways, but doing so just harms themselves.

    function makeFunction(body) {
      mywebguard_log("makeFunction");
        if(body===undefined) throw new Error('makeFunction error: No code to make a function.');
        var locals = body.match(/function\s+\w+\(/g);
        if (locals) {
            body += ';';
            for (var i=0; i<locals.length; ++i) {
                var fname = locals[i].slice(8).match(/\w+/);
                body += 'if(typeof('+fname+')!="undefined")window.'+fname+'='+fname+';';
            }
        }
        return new Function(body);
    }

    // Implement a shadow stack as a list.
    var shadowStack = [];

    // Other code may read (but not write) the current principal.
    thisPrincipal = function() {
        if (shadowStack.length<1) return ''; else
        return shadowStack[shadowStack.length-1];
    };

    // This protected function executes code f at the privileges of a
    // specified principal.
    //revised version supporting AS calls
    function execWith(principal,f) {
      mywebguard_log("execWith");
        if(f==undefined) return;
        if(f===undefined) return;
        shadowStack.push(principal);
        f.apply = builtins.Function.apply;
        try{
          console.log("test")
            var r = f.apply(this,$Array.prototype.slice.call(arguments,2));
        }catch(e){}
        shadowStack.pop();
        //flush_write(principal);
        if (typeof r !== "undefined") return r;
    }

    function execScript(principal, dynamic_script_code){
        mywebguard_log("execScript");
        //alert("execScript -> code= "+ principal+"-----" + dynamic_script_code);
        var dynamic_script = makeFunction(dynamic_script_code); // call our code for turning a string into a global-scoped function
        execWith(principal,dynamic_script);
    }

    /********************** Begin the IRM code ******************************/
    //The common monitor function to intercept a function call with a policy
    var monitorMethod = function(object, method, policy) {
      while (!hasOwnProperty.call(object, method) && object.__proto__)
      object = object.__proto__;
      if (object === null) {
          throw new Error('Failed to find function for alias ' + method);
      }
      var original = object[method];
      if ((original === null) || (original === undefined))
      throw new Error('No method ' + method +'found for '+object);
      //make sure to call the original apply function
      original.apply = builtins.Function.apply;
      object[method] = function wrapper(image) {

          var object = this;
          var orgArgs = arguments;
          var proceed = function() {
            return original.apply(object, orgArgs);
          };
          return policy(orgArgs, proceed,object);
      }
    }
    function setOriginSourceRead(origin){
      try{
        origin_source_read.set(origin,true);
        //alert("Debug: origin '" + origin +"' read data. isOriginSourceRead['"+origin+"']="+origin_source_read.get(origin));
      }catch{
        alert("MyWebGuard-Debug: Error: cannot set origin_source_read for " + origin);
      }
    }
    function isOriginSourceRead(origin){
      //alert("Debug: isOriginSourceRead['"+origin+"']="+origin_source_read.get(origin));
      return origin_source_read.get(origin);
    }

    function getCodeOrigin(trace){
      var url;
      try {
       url = new URL(getCodeSource(trace));
       return url.origin;
      }catch{
        return undefined;
      }
    }
    function isRelativePath(path){
      //alert("Debug: isNotRelativePath('"+path+"')="+ (path && path.indexOf("://")>0 ));
      if(path && path.indexOf("://")>0 ){
        return false;
      }
      return true;
    }
    function originAllowed(origin,objectnName,functionORproperty,args){
      //TODO: implement specific rules
      //alert("Debug: origin '" + origin + "' invokes " + objectnName + "." + functionORproperty + " is allowed");
      return true;
    }
    function isSameOrigin(url1,url2){
      try{
        var same = ((new URL(url1)).origin === (new URL(url2)).origin);
        return same;
      }catch{
        return false;
      }
    }
    function getCodeSource(trace){
      //TODO: need to consider the case of extensions or without HTTP/S URLs
      if (!trace || !trace.includes("http")) {
        return undefined;
      }
      //mywebguard_log("getCodeSource->trace="+trace);
      var protocol;
      var stackLines;
      if (trace.includes("https")) {
        protocol = "https";
        stackLines= trace.split("https://"); 
      }else if (trace.includes("http")) {
        protocol = "http";
        stackLines= trace.split("http://"); 
      }
      if (!stackLines || stackLines.length == 0) {
        return undefined;
      }
      return protocol+"://"+stackLines[stackLines.length-1];
    }
    
    
    function eval_policy(args, proceed, obj) {
      var code = args[0];
      
      mywebguard_log("eval is monitored. code="+code);
      var callstack = new Error().stack;
       mywebguard_log("source=" + getCodeSource(callstack));
      //return proceed();
      return;
    }
    function monitor_location_search() {
      var location_search_desc= Object.getOwnPropertyDescriptor(location, "search");
      Object.defineProperty(location, "search", 
        {
          get: function () {
            var callstack = new Error().stack;
            mywebguard_log(" location.search is monitored. source ="+getCodeSource(callstack));
            return location_search_desc.get.call(this);
        }
      });
    }
    //A. monitoring the sources, where data might be accessed.

    //1. document.getElementById:
    function getElementById_policy(args, proceed, obj) {
      var elementID = args[0];
      var callstack = new Error().stack;
      //mywebguard_log("getElementById is monitored. source ="+getCodeSource(callstack));
      var code_origin = getCodeOrigin(callstack);
      if (originAllowed(code_origin,"document","getElementById",args)) {
        setOriginSourceRead(code_origin);
        return proceed();  
      }
      return;
    }    
    monitorMethod(document, "getElementById", getElementById_policy);
    
    //2. localStorage.getItem

    function localStorage_getItem_policy(args, proceed, obj) {
      var itemID = args[0];
      var callstack = new Error().stack;
      mywebguard_log("localStorage->getItem is accessed. Code from ="+getCodeSource(callstack));
      var code_origin = getCodeOrigin(callstack);
      if (originAllowed(code_origin,"localStorage","getItem",args)) {
        setOriginSourceRead(code_origin);
        return proceed();  
      }
      return;
    }
    monitorMethod(localStorage, "getItem", localStorage_getItem_policy);
    
    //3. monitor document.cookie read and write
    function monitor_document_cookie() {
      var document_cookie_orginal_desc= Object.getOwnPropertyDescriptor(Document.prototype, "cookie") ||
                                          Object.getOwnPropertyDescriptor(HTMLDocument.prototype, 'cookie');
      if (document_cookie_orginal_desc === undefined || !document_cookie_orginal_desc.configurable ||
        !document_cookie_orginal_desc.set || !document_cookie_orginal_desc.get) {
        mywebguard_log("Cannot monitoring document.cookie");
        return;
      }                                  
      Object.defineProperty(document, "cookie", 
        {
          get: function () {
            var callstack = new Error().stack;
            mywebguard_log(" document.cookie is getted. Code from ="+getCodeSource(callstack));
            if (document_cookie_orginal_desc.get.call !== builtins.Function.call){
              document_cookie_orginal_desc.get.call = builtins.Function.call; //ensure to get the original prototype
              alert("Debug: restoring document_cookie_orginal_desc.get.call");
            }
            var code_origin = getCodeOrigin(callstack);
            if (originAllowed(code_origin,"document","cookie","get")) {
              setOriginSourceRead(code_origin);
              return document_cookie_orginal_desc.get.call(document);
            }
            return; 
          },
          set: function(val){
            var callstack = new Error().stack;
            mywebguard_log("document.cookie is set. source ="+getCodeSource(callstack));
            if (document_cookie_orginal_desc.set.call !== builtins.Function.call){
              document_cookie_orginal_desc.set.call = builtins.Function.call; //ensure to get the original prototype
              alert("Debug: restoring document_cookie_orginal_desc.set.call");
            }
            document_cookie_orginal_desc.set.call(document,val);
          },
          enumerable : false, 
          configurable : false
        }
      );
      mywebguard_log("document.cookie access is being monitored");
    }
    monitor_document_cookie();

    //4. monitor window.history read
    function monitor_window_history() {
      var window_history_orginal_desc= Object.getOwnPropertyDescriptor(window, "history");
      if (window_history_orginal_desc === undefined || 
          !window_history_orginal_desc.configurable ||
          !window_history_orginal_desc.get) {
        mywebguard_log("Cannot monitoring window.history");
        return;
      }                                  
      Object.defineProperty(window, "history", 
        {
          get: function () {
            var callstack = new Error().stack;
            mywebguard_log(" window.history is getted. Code from ="+getCodeSource(callstack));
            if (window_history_orginal_desc.get.call !== builtins.Function.call){
              window_history_orginal_desc.get.call = builtins.Function.call; //ensure to get the original prototype
              alert("Debug: restoring window_history_orginal_desc.get.call");
            }
            var code_origin = getCodeOrigin(callstack);
            if (originAllowed(code_origin,"window","history","get")) {
              setOriginSourceRead(code_origin);
              return window_history_orginal_desc.get.call(window);
            }
            return; 
          },
          enumerable : false, 
          configurable : false
        }
      );
      mywebguard_log("window.history access is being monitored");
    }
    monitor_window_history();

    //5. navigator.geolocation
    //https://www.w3schools.com/jsref/obj_geolocation.asp
    /*
    function localStorage_getItem_policy(args, proceed, obj) {
      var itemID = args[0];
      var callstack = new Error().stack;
      mywebguard_log("localStorage->getItem is accessed. Code from ="+getCodeSource(callstack));
      var code_origin = getCodeOrigin(callstack);
      if (originAllowed(code_origin,"localStorage","getItem",args)) {
        setOriginSourceRead(code_origin);
        return proceed();  
      }
      return;
    }
    monitorMethod(navigator.geolocation, "getCurrentPosition", localStorage_getItem_policy);
    */



    //B. monitoring the sinks:
    //reference: https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Sending_forms_through_JavaScript

    //1. Ajax channel:
    /*Policy:
      a. relative path -> allowed
      b. same origin URL -> allowed 
      c. different origin URL (assume CORS is allowed)
         i. if (data is read){
            ask the user and take action according
         }
         ii. if same origin with the code source URL -> allowed
            
         ii. different origin with the code source URL -> ask the user
              
    */
    function XHROpen_policy(args, proceed, obj) {
      var url = args[1];
      mywebguard_log("XMLHttpRequest.open->url=" + url);
     // case: the url origin is different from the host_origin
      var callstack = new Error().stack;
      mywebguard_log(" XMLHttpRequest.open is monitored. source ="+getCodeSource(callstack));
     
      var code_origin = getCodeOrigin(callstack);
      if (code_origin===undefined) {
        throw new Error('Unknown origin to do Ajax');
      }
      //alert("Debug: Ajax, url='"+url+"' host_origin="+host_origin+",code_origin="+code_origin);
      if (isSameOrigin(host_origin,code_origin)) {
        //alert("Debug: Ajax from the same code origin");
        if (isOriginSourceRead(code_origin) && 
            !(isRelativePath(url) || 
              isSameOrigin(url,host_origin))) {
            // data is already read: ask the user:
            if (confirm("MyWebGuard: Sensitive data have been read and a request is about to be sent to '"+url+"' from '"+code_origin+"'. Click OK to allow!")) {
              return proceed();
            } else {
              mywebguard_log('Ajax request is denied by the user');
              return;
            }
        }
        //allowed otherwise
        return proceed();  
      }
      //Ajax from third-party:
      //to the first party, prevent to avoid CSRF attacks:
      //a. relative path or same origin path
      if (isRelativePath(url) || 
          isSameOrigin(url,host_origin)) {
          mywebguard_log("Ajax to '"+url+"' from '"+code_origin+"'. Disallowed by MyWebGuard to prevent potential CSRF!");
          return;
      }
      if (isOriginSourceRead(code_origin)) {
        // data is already read: disallowed
        mywebguard_log("From a third-party code '"+code_origin+"': ajax is sent after sensitive data is read. Disallowed!");
        return;
      }
      if (isSameOrigin(url,code_origin)) {
        return proceed();
      }
      //otherwise, ask the user
      if (confirm("MyWebGuard: A request is about to be sent to '"+url+"' from '"+code_origin+"'. Click OK to allow!")) {
        return proceed();
      } else {
        throw new Error('Ajax request is denied by the user');
      }
      throw new Error('Ajax request is denied by MyWebGuard');
    }
    monitorMethod(XMLHttpRequest.prototype, "open", XHROpen_policy);
    
    //2. Image channel to send data
    function isURLwithData(url){
        if (isRelativePath(url)) {
          return false;
        }
        try{
          var urlObj = new URL(url);
          if (urlObj.search && urlObj.search.length>0) {
            return true;
          }
        }catch{
          return false;
        }
        return false;
    }
    var imgpolicy = {
          get: function(obj, prop) {
            if (prop === "target") {
              return obj;
            }
            return obj[prop];
          },
          set: function(obj, prop, value) {
            if (prop === 'src') {
              //mywebguard_log('Image.src = ' + value);
              //obj[prop]=value; return obj; // uncomment this line to test without stack
              var callstack = new Error().stack;
              var code_origin = getCodeOrigin(callstack);
              mywebguard_log("Image().src='"+value+"' is called. Code from " + getCodeSource(callstack));
              if (isURLwithData(value) && isOriginSourceRead(code_origin)) {
                //supicious image source with data and sensitive data have been read by the code origin
                //ask the user
                if (!confirm("MyWebGuard: Sensitive data have been read and supicious image source with data  '"+value+"' from '"+code_origin+"'. Click OK to allow!")) {
                  value = "";
                  return;
                } 
              }
              obj[prop]=value;
             }
             return obj;
           }
    };
    function createElement_policy(args, proceed, obj) {
      var elementType = args[0];
      var elementObject = proceed(); 
      mywebguard_log("document.createElement is called. elementType="+elementType);
      //var callstack = new Error().stack;
      //mywebguard_log("document.createElement is called. source=" + getCodeSource(callstack));
      //return elementObject;       //just testing for Facebook, it works for Messenger, broken otherwise

      if (elementType === "img") {
        //mywebguard_log("img type found");
        return new Proxy(elementObject, imgpolicy);
      }
      return elementObject;
    }
    function ImageObjectMonitor(){
      mywebguard_log("ImageObjectMonitor() is called");
      var NativeImage = Image;
      class FakeImage {
        constructor(height, width) {
          var imgObject = new NativeImage(height,width);
          imgObject = new Proxy(imgObject,imgpolicy);
          return imgObject;
        }
      }
      Image = FakeImage;
      //mywebguard_log("ImageObjectMonitor():Image="+Image);
    }
    ImageObjectMonitor();
    
    //3. WebSocket
    

    function WebSocketMonitor(){
      mywebguard_log("WebSocketMonitor is called");
      var NativeWebSocket = WebSocket;
      class FakeWebSocket {
        constructor(url) {
          var wsObject = new NativeWebSocket(url);
          //return wsObject; //uncomment this line to test without stack
          mywebguard_log("WebSocket is intercepted with url="+url);
          var callstack = new Error().stack;
          //mywebguard_log("WebSocket is call. Code from ="+getCodeSource(callstack));
          var code_origin = getCodeOrigin(callstack);
          if ( isOriginSourceRead(code_origin) && 
              (!isSameOrigin(url,host_origin) || !isSameOrigin(host_origin,code_origin ))) {
            if (confirm("MyWebGuard: Sensitive data have been read and a request is about to be sent to '"+url+"' from '"+code_origin+"'. Click OK to allow!")) {
              return wsObject;
            } else {
              mywebguard_log("WebSocket to '"+url + "' from '"+code_origin+"' is blocked");
              return;
            }
          }
          return wsObject;  
        }
      }
      WebSocket = FakeWebSocket;      
    }
    //monitorMethod(window.WebSocket.prototype, "send", WebSocketsend_policy);
    WebSocketMonitor();


  //4. Window history
  
         function HistoryMonitor(){
         window.onpopstate = function (event) {
         if (event.state) {
         mywebguard_log(" history changed because of pushState/replaceState ");
         } else {
         // history changed because of a page load
        }
        }
        }
        HistoryMonitor();


    //C. DOM modification:
    monitorMethod(document, "createElement", createElement_policy);

    function appendChild_policy(args, proceed, obj) {
      var child = args[0];
      if (child.target !== undefined && child.target.tagName === "IMG") {
        args[0] = child.target;
      }
      return proceed();
    }
    monitorMethod(document, "appendChild", appendChild_policy);

    //D. other
    //1.
    monitorMethod(window, "eval", eval_policy);
    //document.write[ln]
    mywebguard_log("mywebguard.js is completely loaded");
 }
  catch (err) {
    alert(err.message);
  }
})();
`;
document.documentElement.appendChild(injectee);