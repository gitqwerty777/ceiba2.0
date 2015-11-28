

























self.port.on('parseCourse', function(){
    console.log("parsecourse");

    //var tables = document.getElementsByTagName("table");
    
    var tables = $("table");
    var availableTable = tables[0];
    var rows = Array.from(availableTable.rows);
    rows.forEach(function(r, ri){
	var cellArray = Array.from(r.cells);
	cellArray.forEach(function(c, ci){
	    if(ci == 4)
		console.log(c.innerHTML);
	});
    });
    console.log("table: ", tables[0].rows[0].cells[0].innerHTML);//學期
    //var rows = tables[0];
    //console.log(rows);
    //var last = rows[rows.length - 1];
    //var cell = last.cells[0];
    //var value = cell.innerHTML
});

self.port.on('init', function(){
   console.log("init");
    $(".btn").click();
});

self.port.on('login', function(){
    console.log("login");
    //$("input.text").appendTo('body').get(0).checked
    var inputuser1 = $('input[type="text"]');
    inputuser1.val("b01902059");
    var inputuser2 = $('input[type="password"]');
    inputuser2.val(mypassword);
    var btn = $('input[type="submit"]');
    btn.click();
});
