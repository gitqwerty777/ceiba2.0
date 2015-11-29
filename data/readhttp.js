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
		
			var str = c.innerHTML;			
			var st = str.search('http');
			if(st==-1)
				break;
			var en ;
			for(en=st+1;str[en]!='"';++en);
			var gethttp = str.slice(st,en);
			console.log("!!"+gethttp+"!!");
			c.innerHTML+="<br>"+gethttp;
			
		}
	};
    });
    
	deleteSelectedColoumns();
});

