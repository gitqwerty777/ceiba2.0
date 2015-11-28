function showceibaweb(){
	window.open("https://ceiba.ntu.edu.tw/student/",'_blank');
}

function createButton(context, func){
    var button = document.createElement("input");
    button.type = "button";
    button.value = "go to ceiba";
    button.onclick = func;
    context.appendChild(button);
}

window.onload = function(){
    createButton(document.body, function(){
        //highlight(this.parentNode.childNodes[1]);
        // Example of different context, copied function etc
         createButton(this.parentNode, this.onclick);
		 showceibaweb();
    });
}
