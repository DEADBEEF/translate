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

var dirty_translate = false;
var dirty_notes = false;

function update_translation() {
    var loc = window.location.pathname.split("/");
    var translation = $('#translation').val();
    xss_protect();
    $.post("/update/page/", {translation:translation,
    notebook:loc[2], story:loc[3],page:loc[4]}
    , function() {
        dirty_translate = false;
    });
};

$(document).ready(function () {
    $("#image_container").bind("click", function() {
        $("#image_container > img").toggleClass("zoom");
    });
    $("button").bind('click', update_translation);

});
