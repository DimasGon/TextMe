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