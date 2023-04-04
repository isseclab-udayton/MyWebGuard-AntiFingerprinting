var injectee = document.createElement("script");
injectee.innerHTML = `
(function () {
	var host_origin = (new URL(window.location)).origin;
	var CORS_enabled = 'withCredentials' in new XMLHttpRequest();
	var origin_source_read = new Map();
	var debug = true;
	function mywebguard_log(s) {
		// if ((!debug) || (!console.log)) return;
		console.log('mywebguard log: ' + s);
	}
	mywebguard_log("starting mywebguard.js");
	var $Array = Array;
	var $Object = window.Object;
	var hasOwnProperty = Object.prototype.hasOwnProperty;
	var originalDocument_createElelment = document.createElement;
	var builtins = {};
	builtins.__proto__ = null;
	with (Function.prototype)
	builtins.Function = { apply: apply, call: call, toString: toString };
	try {
		function makeFunction(body) {
			mywebguard_log("makeFunction");
			if (body === undefined) throw new Error('makeFunction error: No code to make a function.');
			var locals = body.match(/function\\s+\\w+\\(/g);
			if (locals) {
				body += ';';
				for (var i = 0; i < locals.length; ++i) {
					var fname = locals[i].slice(8).match(/\\w+/);
					body += 'if(typeof(' + fname + ')!="undefined")window.' + fname + '=' + fname + ';';
				}
			}
			return new Function(body);
		}
		var shadowStack = [];
		thisPrincipal = function () {
			if (shadowStack.length < 1) return ''; else
				return shadowStack[shadowStack.length - 1];
		};
		function execWith(principal, f) {
			mywebguard_log("execWith");
			if (f == undefined) return;
			if (f === undefined) return;
			shadowStack.push(principal);
			f.apply = builtins.Function.apply;
			try {
				console.log("test")
				var r = f.apply(this, $Array.prototype.slice.call(arguments, 2));
			} catch (e) { }
			shadowStack.pop();
			if (typeof r !== "undefined") return r;
		}

		function execScript(principal, dynamic_script_code) {
			mywebguard_log("execScript");
			var dynamic_script = makeFunction(dynamic_script_code); // call our code for turning a string into a global-scoped function
			execWith(principal, dynamic_script);
		}

		var monitorMethod = function (object, method, policy) {
			while (!hasOwnProperty.call(object, method) && object.__proto__)
				object = object.__proto__;
			if (object === null) {
				throw new Error('Failed to find function for alias ' + method);
			}
			var original = object[method];
			if ((original === null) || (original === undefined))
				throw new Error('No method ' + method + 'found for ' + object);
			original.apply = builtins.Function.apply;
			object[method] = function wrapper(image) {

				var object = this;
				var orgArgs = arguments;
				var proceed = function () {
					return original.apply(object, orgArgs);
				};
				return policy(orgArgs, proceed, object);
			}
		}
		function setOriginSourceRead(origin) {
			try {
				origin_source_read.set(origin, true);
			} catch {
				alert("MyWebGuard-Debug: Error: cannot set origin_source_read for " + origin);
			}
		}
		function isOriginSourceRead(origin) {
			return origin_source_read.get(origin);
		}

		function getCodeOrigin(trace) {
			var url;
			try {
				url = new URL(getCodeSource(trace));
				return url.origin;
			} catch {
				return undefined;
			}
		}
		function isRelativePath(path) {
			if (path && path.indexOf("://") > 0) {
				return false;
			}
			return true;
		}
		function originAllowed(origin, objectnName, functionORproperty, args) {
			return true;
		}
		function isSameOrigin(url1, url2) {
			try {
				var same = ((new URL(url1)).origin === (new URL(url2)).origin);
				return same;
			} catch {
				return false;
			}
		}
		function getCodeSource(trace) {
			if (!trace || !trace.includes("http")) {
				return undefined;
			}
			var protocol;
			var stackLines;
			if (trace.includes("https")) {
				protocol = "https";
				stackLines = trace.split("https://");
			} else if (trace.includes("http")) {
				protocol = "http";
				stackLines = trace.split("http://");
			}
			if (!stackLines || stackLines.length == 0) {
				return undefined;
			}
			return protocol + "://" + stackLines[stackLines.length - 1];
		}


		function eval_policy(args, proceed, obj) {
			var code = args[0];

			mywebguard_log("eval is monitored. code=" + code);
			var callstack = new Error().stack;
			mywebguard_log("source=" + getCodeSource(callstack));
			return;
		}
		function monitor_location_search() {
			var location_search_desc = Object.getOwnPropertyDescriptor(location, "search");
			Object.defineProperty(location, "search",
				{
					get: function () {
						var callstack = new Error().stack;
						mywebguard_log(" location.search is monitored. source =" + getCodeSource(callstack));
						return location_search_desc.get.call(this);
					}
				});
		}
		function canvasElement_policy(args, proceed, obj) {
			var element = proceed()
			// assign next policy if element is canvas
			if (isCanvasElement(element)) {
				//Monitor accesses to the canvas element
				console.log("[MyWebGuard][ALERT] Canvas element detected, monitoring the element...")
				monitorMethod(element, "getContext", getContext_policy);
				monitorMethod(element, "toDataURL", toDataURL_policy);
			}
			return element
		}
		monitorMethod(document, "getElementById", canvasElement_policy);
		monitorMethod(document, "createElement", canvasElement_policy);
		
		function getContext_policy(args, proceed, obj) {
			var ctx = proceed()
			monitorMethod(ctx, "fillText", fillText_policy);
			return ctx
		}
		
		function toDataURL_policy(args, proceed, obj) {
			var ctx = obj.getContext("2d")
			if (!canvasAllowed(ctx, "HTMLCanvasElement", "toDataURL", args)) {
				poisonCanvas(ctx)
			}
			return proceed()
		}
		
		function fillText_policy(args, proceed, obj) {
			// Proceed first, this guarantees our poison is drawn last
			proceed()
			// Poison canvas if it does not pass our policies
			if (!canvasAllowed(obj, "CanvasRenderingContext2D", "fillText", args)) {
				poisonCanvas(obj)
			}
			return
		}
		
		// Returns true if element is canvas
		function isCanvasElement(element){
			return element !== null && element.tagName.toLowerCase() == "canvas"
		}
		
		function canvasAllowed(ctx, objectName, functionName, args) {
			if (!canvasInViewport(ctx.canvas)) {
				console.log('[NOTICE] Canvas Element is NOT in the viewport!')
				return false
			}
		
			if (ctx.canvas.style.zIndex < 0) {
				console.log('[NOTICE] Canvas Element has a negative z-axis!');
				return false;
			}
			var callstack = new Error().stack;
			var code_origin = getCodeOrigin(callstack);
			if (!originAllowed(code_origin, objectName, functionName, args)) {
				console.log('[NOTICE] Canvas Element has disallowed origin!');
				return false;
			}
			return true
      		//return false
		}
		
		function canvasInViewport(canvasElement) {
			var bounding = canvasElement.getBoundingClientRect()
		
			var inViewportTop = bounding.top >= 0
			var inViewportLeft = bounding.left >= 0
			var inViewportRight = bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
			var inViewportBottom = bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight)
		
			return inViewportTop && inViewportLeft && inViewportRight && inViewportBottom
		}
		
		function poisonCanvas(ctx) {
			poisonText = (+new Date).toString(36);
			var x = Math.random()*ctx.canvas.width;
			var y = Math.random()*ctx.canvas.height;
			ctx.font = "10px Arial";
			ctx.strokeText(poisonText, x, y);
		}
		// Anti-PingLoc Policies ----------------------------------------------------------------------------------------------------------
		function monitor_ping(){
			var HTMLImageElement_src_orginal_desc = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, "src")
			Object.defineProperty(HTMLImageElement, "src",
				{
					// not used for mitigation, but necessary to implement
					get: function () {
						console.log("Image getter intercepted...")
						return HTMLImageElement_src_orginal_desc.get.call(HTMLImageElement);
					},
					// here is where we actually monitor PingLoc. We intercept img.src = ... setting calls
					set: function (val) {
						// policy can be applied here
						console.log("Image setter intercepted...")
						var callstack = new Error().stack;
						var code_origin = getCodeOrigin(callstack);
						if (!originAllowed(code_origin, "img", "src", args)) {
							console.log('[NOTICE] Image element has disallowed origin!');
						}
						// let them collect the data
						HTMLImageElement_src_orginal_desc.set.call(HTMLImageElement, val);
					},
					enumerable: false,
					configurable: false
				}
			);
			mywebguard_log("img.src access is being monitored");
		}
		monitor_ping();
		monitorMethod(window, "eval", eval_policy);
		mywebguard_log("mywebguard.js is completely loaded");
	}
	catch (err) {
		alert(err.message);
	}
})();`;
document.documentElement.appendChild(injectee);