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
		c.innerHTML += "("+ c.innerHTML+ ")";
		
			var str = c.innerHTML;			
			var st = str.search('http');
			if(st==-1)
				break;
			var en ;
			for(en=st+1;str[en]!='"';++en);
			console.log("!!"+str.slice(st,en)+"!!");
		}
	};
    });
    
});

self.port.on('init', function(){
   console.log("init");
    $(".btn").click();
});

self.port.on('login', function(ac,pw){
    console.log("login");
    //$("input.text").appendTo('body').get(0).checked
    var inputuser1 = $('input[type="text"]');
    inputuser1.val(ac);
    var inputuser2 = $('input[type="password"]');
    inputuser2.val(pw);
    var btn = $('input[type="submit"]');
    btn.click();
});

