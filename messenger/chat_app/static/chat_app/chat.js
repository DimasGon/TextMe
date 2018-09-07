var reloadMessages = function () {
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        beforeSend: function () {
            $("#js-insert-new-mes").html(
                `<i class="icon-clockalt-timealt"></i>
                <li class="user-mes">
                    <p>${ $("#input-text").val() }</p>
                </li>`
            );
            alert(form.serialize());
        },
        success: function (data) {
            $("#js-insert-chat").html(data.chat_page)
        }
    })
    return false;
}

$(function () {
    
    $("#js-insert-chat").on("submit", ".js-send-mes", reloadMessages)

})