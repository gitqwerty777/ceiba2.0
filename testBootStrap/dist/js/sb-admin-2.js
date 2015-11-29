
function addNotifications(){
    $(".dropdown-alerts li:eq(0)").before("<li class=\"divider\"></li>");
    $(".dropdown-alerts li:eq(0)").before('<li><a href=\"#\"><div><i class=\"fa fa-comment fa-fw\"></i> New Comment<span class="pull-right text-muted small">4 minutes ago</span></div></a></li>');
}

function addHomeworks(){
   $(".dropdown-tasks li:eq(0)").before("<li class=\"divider\"></li>");
    $(".dropdown-tasks li:eq(0)").before('<li>                            <a href=\"#\">                                <div>                                    <p>                                        <strong>Task 1</strong>                                        <span class=\"pull-right text-muted\">40% Complete</span>                                    </p>                                    <div class=\"progress progress-striped active\">                                        <div class=\"progress-bar progress-bar-success\" role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 40%\"><span class=\"sr-only\">40% Complete (success)</span></div></div></div></a></li>');
}

$(function() {

    $('#side-menu').metisMenu();
    addNotifications();
    addHomeworks();
});


//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url || url.href.indexOf(this.href) == 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }
});
