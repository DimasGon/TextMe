$(function () {

    $.ajax({
        url: '/account/api',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $("#js-insert-acc").html(data.html_page);
        }
    });

    $.ajax({
        url: '/account/api/bookmarks',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $("#js-insert-bookmarks").html(data.html_page);
        }
    });
  
});

$("#js-insert-acc").on("submit", ".js-add-post", function () {
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            $("#js-insert-acc").html(data.html_page);
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
            $("#js-insert-acc").html(data.html_page);
        }
    });
    return false;
});

$("#js-insert-acc").on("submit", ".js-add-bookmarks", function () {
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            $("#js-insert-bookmarks").html(data.html_page);
        }
    });
    return false;
});

$("#js-insert-bookmarks").on("submit", ".js-add-bookmarks", function () {
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            $("#js-insert-bookmarks").html(data.html_page);
        }
    });
    return false;
});
