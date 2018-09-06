$(function () {
    
    $.ajax({
        url: '/chats_api',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $("#js-insert-left-chats").html(data.left_chats);
        }
    });

})