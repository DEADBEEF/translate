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
var active_notes = "page";

function update_translation() {
    var loc = window.location.pathname.split("/");
    var translation = $('#translation').val();
    xss_protect();
    $.post("../../../../update/page/", {translation:translation,
    notebook:loc[2], story:loc[3],page:loc[4]}
    , function() {
        dirty_translate = false;
    });
};

function update_note() {
    if (dirty_notes) {
        var old_notes = $("#note_area").val();
        var loc = window.location.pathname.split("/");
        //Push changes
        dirty_notes = false;
        xss_protect();
        $.post("../../../../update/notes/", {note:old_notes,
            field:active_notes, notebook:loc[2],
            story:loc[3]},
            function(){});
    }
};

function get_note(note){
    var loc = window.location.pathname.split("/");
    $.get("../../../../get/notes/", {field:note, notebook:loc[2],
        story: loc[3]},function (data) {
        $("#note_area").val(data);
        if (note == "project") {
            $("#notes_block h3").html("Project Notes:");
        } else {
            $("#notes_block h3").html("Page " + note + " Notes:");
        }
    });

};

function switch_project() {
    if (active_notes != "project"){
        update_note();
        get_note("project");
        active_notes = "project";
    }
};

function switch_to_page(){
    var to_page = $(this).attr("id");
    if (active_notes != to_page) {
        update_note();
        get_note(to_page);
        active_notes = to_page;
    }
};

function update_server_values() {
    update_note();
    if (dirty_translate){
        update_translation();
    }
    $("#save_block").removeClass("changed");
};

$(document).ready(function () {
    active_notes = $("#current_page").html();
    $("#image_container").bind("click", function() {
        $("#image_container > img").toggleClass("zoom");
    });
    $("button").bind('click', update_translation);
    $("#project_notes").bind('click', switch_project);
    $("#notes_nav li").bind('click', switch_to_page);
    $("#note_area").bind('change',function () {
        dirty_notes = true;
        $("#save_block").addClass("changed");
    });
    $("#translation").bind('change',function () {
        dirty_translate = true;
        $("#save_block").addClass("changed");
    });
    setInterval(update_server_values, 10000);
    $("#save").bind('click', update_server_values);
});
