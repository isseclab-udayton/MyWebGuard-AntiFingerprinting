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

// Policy used when monitoring acesses to a canvas element
// https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
function getContext_policy(args, proceed, obj) {
	var ctx = proceed()
	// assign next policy
	monitorMethod(ctx, "fillText", fillText_policy);
	return ctx
}

// Policy monitoring a canvas element being exported to a data URL
// The data URL has 
// https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toDataURL
function toDataURL_policy(args, proceed, obj) {
	// Get context of HTMLCanvasElement
	var ctx = obj.getContext("2d")
	if (!canvasAllowed(ctx, "HTMLCanvasElement", "toDataURL", args)) {
		poisonCanvas(ctx)
	}
	// Return proceed after poisoning the canvas
	// The Data URL will be unidentifiable since the canvas has been poisoned
	return proceed()
}

// Policy monitoring the fillText method used for rendering text
// The rendered text has hardware-specific anti-aliasing that can be used to fingerprint
// https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fillText
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

// canvasAllowed identifies a suspicious canvas element that may be used for fingerprinting
// ctx is a CanvasRenderingContext2D
function canvasAllowed(ctx, objectName, functionName, args) {
	// Check if canvas element is in the viewport
	if (!canvasInViewport(ctx.canvas)) {
		console.log('[NOTICE] Canvas Element is NOT in the viewport!')
		return false
	}
	// console.log('[NOTICE] Canvas Element is in the viewport.')

	// Check if canvas element is behind the webpage (negative z-axis), canvas element behind the webpage is suspicious
	if (ctx.canvas.style.zIndex < 0) {
		console.log('[NOTICE] Canvas Element has a negative z-axis!');
		return false;
	}
	// console.log('[NOTICE] Canvas Element has a valid z-axis.');

	// Check code origin
	var callstack = new Error().stack;
	var code_origin = getCodeOrigin(callstack);
	if (!originAllowed(code_origin, objectName, functionName, args)) {
		console.log('[NOTICE] Canvas Element has disallowed origin!');
		return false;
	}
	// console.log('[NOTICE] Canvas Element has allowed origin.');

	return true
}

// Check if canvas element is in the viewport, canvas element outside the viewport is suspicious
// From https://awik.io/check-if-element-is-inside-viewport-with-javascript
function canvasInViewport(canvasElement) {
	var bounding = canvasElement.getBoundingClientRect()

	var inViewportTop = bounding.top >= 0
	var inViewportLeft = bounding.left >= 0
	var inViewportRight = bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
	var inViewportBottom = bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight)

	return inViewportTop && inViewportLeft && inViewportRight && inViewportBottom
}

// What if we poison with a linear gradient between two random colors?
// 	- This would guarantee every inch of the canvas is poisoned - lower chance of being covered by attacker
// 	- Avoids the issue of having to call "fillText" in a policy monitoring fillText
// MAKE SURE THIS CALLS THE ORIGINAL FILL TEXT OR WE WILL RECURSE FOREVER BY CALLING OUR POLICY FROM OUR POLICY
function poisonCanvas(ctx) {
	// From https://stackoverflow.com/a/32649933/10053864
	poisonText = (+new Date).toString(36);

	var x = Math.random()*ctx.canvas.width;
	var y = Math.random()*ctx.canvas.height;

	//TODO: Applying a color gradient to the text increases complexity -> stronger poison 
	
	//Source: https://link.springer.com/content/pdf/10.1007/978-3-030-22038-9_3.pdf
	ctx.font = "10px Arial";
	ctx.strokeText(poisonText, x, y); // use strokeText function so we don't infinitely recurse
}