document.write("<script src='/static/js/json2.js'></script>");
document.write("<script src='/static/js/jquery.json.js'></script>");
$(document).ajaxSend(function (event, xhr, settings) {
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

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
var bindclick=function(){
        var thumbnail = document.getElementById("pictures");
    var li = thumbnail.getElementsByTagName("li");
    for (var i = 0; i < li.length; i++) {
        li[i].onclick = function () {
            if (this.className == "") {
                this.className = "checked";
            }
            else if (this.className == "checked") {
                this.className = "";
            }
        }
    }
}
$(document).ready(function () {

    $('#taging').click(function () {
        var len = $(".checked").length;
        var i = 0;
        var arrayid = new Array();
        $(".checked").each(function () {
            arrayid.push($(this).attr("id"));
        })
        var keyid = $(".keyinfo").attr('id');
        var studentid = $(".studentid").attr('id');
        var pictureindex = $(".picindex").attr('id');
        var response = { picindex: pictureindex, wordid: keyid, picids: arrayid, studentid: studentid }
        var json_log = JSON.stringify(response);
        $.post('/annotation/process', response,
            function (data) {
                data = JSON.parse(data);
                var keyid = data.keyid;
                var keyword = data.keyword;
                var picindex = data.picindex;
                var piclist = data.picture_list;

                $(".keyinfo").text(keyword);
                $(".keyinfo").attr("id",keyid);

                $(".picindex").attr("id",picindex);
                $("#thumbnail").empty();
                var piclist = data.picture_list;

//                $("#picpanel").empty();
                var $pictureselems = $("<ul class='thumbnails grid' id='pictures'></ul>");

                $.each(piclist, function () {
                    var $lielem = $("<li class=''></li>");
                    $lielem.attr("id", this.id);
                    var $imgelem = $("<img class='img-polaroid'/>");
//                    $imgelem.attr("src", "/media/" + this.src);
                    $imgelem.attr("src", this.src);
                    $lielem.append($imgelem);
                    $pictureselems.append($lielem);
                });
                $("#thumbnail").append($pictureselems);



//                var $picindexelem = $("<div class='row-fluid picindex'></div>");
//                $picindexelem.attr("id", picindex);
//                var $studentelem = $("<div class='span4 studentid pull-left'></div>");
//                $studentelem.attr("id", studentid);
//                var $keyelem = $("<h1 class='keyinfo'></h1>");
//                $keyelem.attr("id", keyid);
//                $keyelem.text(keyword);
//                $studentelem.append($keyelem);
//                var $rowelem=$("<div class='row-fluid'></div>");
//                $rowelem.append($studentelem);
//                $picindexelem.append($rowelem);
//                $picindexelem.append($("<hr>"));
//
//                $("#picpanel").append($picindexelem);
//
//                //add pictures
//                var $picelems = $("<div class='row-fluid'></div>");
//                var $thumbnailelem = $("<div class='span11' id='thumbnail'></div>");
//                var $pictureselems = $("<ul class='thumbnails grid' id='pictures'></ul>");
//
//                $.each(piclist, function () {
//                    var $lielem = $("<li class=''></li>");
//                    $lielem.attr("id", this.id);
//                    var $imgelem = $("<img class='img-polaroid'/>");
//                    $imgelem.attr("src", "/media/" + this.src);
//                    $lielem.append($imgelem);
//                    $pictureselems.append($lielem);
//                });
//                $thumbnailelem.append($pictureselems);
//                $picelems.append($thumbnailelem);
//                $("#picpanel").append($picelems);
                bindclick();
            });
    });
    bindclick();
});
