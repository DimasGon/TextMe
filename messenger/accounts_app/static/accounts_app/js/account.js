$(function () {

    $.ajax({
        url: '/account/api',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $("#js-insert-acc").html(data.html_page);
        }
    });
  
});

$("#js-insert-acc").on("submit", ".js-add-bookmarks", function () {
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            if (data.added) {
                alert("Добавлен");
            }
            else {
                alert("Не добавлен");
            }
        }
    });
    return false;
});

$("#js-insert-acc").on("submit", ".js-add-post", function () {
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            $("#wallposts").html(data.wall);
        }
    });
    return false;
});

$("#js-insert-acc").on("submit", ".js-add-comment", function () {
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            alert("Коммент добавлен");
        }
    });
    return false;
});