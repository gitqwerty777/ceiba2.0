var self = require('sdk/self');
var tabs = require("sdk/tabs");
var buttons = require('sdk/ui/button/action');
var data = require("sdk/self").data;

var button = buttons.ActionButton({
    id: "mozilla-link",
    label: "Visit New Ceiba",
    icon: {
	"16": "./icon-16.png",
	"32": "./icon-32.png",
	"64": "./icon-64.png"
    },
    onClick: handleClick
});


function getWorker(){
    return tabs.activeTab.attach({
	contentScriptFile: [
	    data.url("jquery-1.11.3.min.js"),
	    data.url("autologin.js")
	],
    });
}

function readdataline(str){
	var arr = new Array();
	console.log(str.split(/^(?= [1-9] |[1-9][0-9] )/m));
	arr.push(str.split(/^(?= [1-9] |[1-9][0-9] )/m));
	return arr;

}

tabs.on('ready', function(tab) {
    //console.log('tab is loaded', tab.title, tab.url);
    if(tab.url == "https://ceiba.ntu.edu.tw/"){
	var worker = getWorker();
	worker.port.emit("init");
    } else if(tab.url == "https://web2.cc.ntu.edu.tw/p/s/login2/p1.php"){
	var worker = getWorker();
		var ac = data.load("logac.data"),
			pw =data.load("logpw.data");
	worker.port.emit("login", ac,pw);
    } else if(tab.url == "https://ceiba.ntu.edu.tw/student/index.php" || tab.url == "https://ceiba.ntu.edu.tw/student/"){
	var worker = getWorker();
	worker.port.emit("parseCourse");
    }
});

function handleClick(state) {
    tabs.open("https://ceiba.ntu.edu.tw/");
}

var ss = require("sdk/simple-storage");
ss.storage.account = "b01902059";
ss.storage.password = "password";


