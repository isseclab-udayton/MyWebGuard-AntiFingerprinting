// Block ad with id=name
function blockID(name) {
	e = document.getElementById(name);
	e.innerHTML = `<p>Ad blocked by stallj2 (identified by id="${name}")</p>`;
}

// Block ad with class=name
function blockClass(name) {
	blockElements = document.getElementsByClassName(name);
	for (e of blockElements) {
		e.innerHTML = `<p>Element blocked by stallj2 (identified by class="${name}")</p>`;
	}
}

blockID("ad");
blockClass("ad");

window.og_alert = window.alert;

alerts = 0;
alerts_ok = true;

window.alert = function (msg) {
	alerts++

	if (alerts == 3) {
		alerts_ok = confirm("Do you want to allow this site to keep alerting you?");
	}

	if (alerts >= 3 && !alerts_ok) {
		console.log("Alert blocked.");
		console.log("Tried to alert with message: " + msg);
		return
	}

	alert(msg)
};

// window.alert = window.og_alert