/**js submit post request: hidden request parameters**/
function postDetail(URL, PARAMTERS) {
    //Create a form form
    var temp_form = document.createElement("form");
    temp_form.action = URL;

    temp_form.method = "post";
    temp_form.style.display = "none";
    //add parameters
    for (var item in PARAMTERS) {
      var opt = document.createElement("textarea");
      opt.Hash = PARAMTERS[item].Hash;
      temp_form.appendChild(opt);
    }
    document.body.appendChild(temp_form);
    //submit data
    temp_form.submit();
  }