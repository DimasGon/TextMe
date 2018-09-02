const Chats = ({id, first_name, second_name, last_message_text, last_message_time, avatar}) => (
    `<a href="/chat/${ id }">
        <div class="left-content btm-border">
            <img src="${ avatar }">
            <h5>${ first_name } ${ second_name }</h5>
            <p>${ last_message_text }</p>
            <span>${ last_message_time }</span>
        </div>
    </a>`
)

const renderChat = res => {
    chats_html = res.data.result.map(Chats).join('')
    container = document.getElementById('chats')
    container.innerHTML = chats_html
}