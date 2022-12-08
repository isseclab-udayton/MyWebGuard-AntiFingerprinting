// Prevent canvas fingerprinting
function getImageData_policy(args, proceed, obj) {
	var elementID = args[0];
	var callstack = new Error().stack;
	//mywebguard_log("getElementById is monitored. source ="+getCodeSource(callstack));
	var code_origin = getCodeOrigin(callstack);

	// Our condition
	// This will decide if the function is allowed to continue or gets blocked
	if ("they are nice") {
		return proceed(); // calls original function
	}
	return;
}
monitorMethod(document, "getImageData", getElementById_policy);

// getImageData, toDataURL

var fontLoads = 0
var fontLoadLimit = 10

function checkFontLoad() {
	fontLoads++
	return fontLoads > fontLoadLimit
}

function ourOriginAllowed() {
	// use steven black blocklist?
}

