const Chats = ({id, first_name, second_name, avatar}) => (
    `<a href="/chat/${ id }">
        <div class="left-content btm-border">
            <img src="${ avatar }">
            <h5>${ first_name } ${ second_name }</h5>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing</p>
        </div>
    </a>`
)

const renderChat = res => {
    chats_html = res.data.result.map(Chats).join('')
    container = document.getElementById('chats')
    container.innerHTML = chats_html
}