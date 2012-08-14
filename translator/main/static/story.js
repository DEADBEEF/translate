function xss_protect(){
    $('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
    });
};

$(document).ready(function () {
	$("#tabs li").bind('click', function() {
		var index = $(this).index();
		$("#tabcontents .content").removeClass("selected");
		$("#tabs li").removeClass("selected");
		$(this).addClass("selected");
		var a = $("#tabcontents .content").get(index);
		$(a).addClass("selected");

	});
    $("#project").bind('click', function() {
        var loc = window.location.pathname.split("/");
        xss_protect();
        $.post("../../../project/start/", {"book": loc[2],
            "story":loc[3]},
            function(result) {
                $("#project").remove();
                $('.transopt').append("<div id=\"project_started\">Translation Project Started</div>");
                $('#tabContainer > #tabs > ul').append("<li>Project Notes</li>");
                $('#tabContainer > #tabcontents').append("<div class=\"content\"></div>");
                $("#tabs li").bind('click', function() {
		        var index = $(this).index();
		        $("#tabcontents .content").removeClass("selected");
		        $("#tabs li").removeClass("selected");
		        $(this).addClass("selected");
		        var a = $("#tabcontents .content").get(index);
		        $(a).addClass("selected");
                });
        });
    });
});
