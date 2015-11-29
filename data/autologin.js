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

