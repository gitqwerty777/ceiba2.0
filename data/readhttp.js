function deleteSelectedColoumns() {
	console.log("start delete");
    var table= $('table'); //html table
	var tb=table[0]; 
    var NoOfcolumns = tb.rows[0].cells.length; //no. of columns in table 
    for (var clm = NoOfcolumns-1; clm >=0; clm--) {
		if(clm==4)
			continue;
		console.log("eating column "+clm);
        var rw = tb.rows[0]; //0th row with checkboxes
		var lastrow = tb.rows;
		for (var x = 0; x < lastrow.length; x++) {
			tb.rows[x].deleteCell(clm);
		}
        
    }
}

function getpage(url){
var req = new XMLHttpRequest();

req.open('GET', url, false);
req.send(null);
//if(req.status == 200) 
	return req.responseText;
}

function httpstr(page){
	var st = page.search("https");
	if(st==-1)
		return "NO find HTTP";
	var en;
	for(en=st+1;page[en]!='"';++en);
	return page.slice(st,en);
}
self.port.on('parseCourse', function(){
    console.log("parsecourse");

    //var tables = document.getElementsByTagName("table");
    
    var tables = $("table");
    var availableTable = tables[0];
    var rows = Array.from(availableTable.rows);
    rows.forEach(function(r, ri){
	var cellArray = Array.from(r.cells);
//	cellArray.forEach(function(c, ci){
	for(var ci=0;ci<cellArray.length;++ci){
	    if(ci == 4){
		var c = cellArray[ci];
		console.log(c.innerHTML);
		var updateCount = ri;
//		c.innerHTML += "("+ c.innerHTML+ ")";
		
		var gethttp=httpstr(c.innerHTML);
		if(gethttp=="NO find HTTP")
			break;
			console.log("!!"+gethttp+"!!");
			c.innerHTML+="<br>"+httpstr(getpage(gethttp));
			
		}
	};
    });
    
	deleteSelectedColoumns();
});

