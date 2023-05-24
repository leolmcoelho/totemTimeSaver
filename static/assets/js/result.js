
let item = localStorage.getItem('status-bot'),
    message = document.querySelector('.message'),
    vector = document.querySelector('.vector'),
    error = `<div class="alert alert-danger" role="alert">
Amil: Erro no Token
</div>`;

if (item == 200) {
    var text = 'Atendimento concluído com sucesso!<br>Aguarde ser chamado(a) para sua consulta.'

    var path = 'Vector_true';
}
else {
    text = 'Erro no processamento. Por favor, dirija-se a recepção.'
    'Erro no processamento. Por favor, dirija-se a recepção.'
    var path = 'Vector';

    var errorText = localStorage.getItem('error');
    //console.log(errorText);

    if (errorText) {
        var errorContainer = document.querySelector("#error");
        //console.log(errorContainer);
        var errorDiv = document.createElement("div");
        errorDiv.className = "alert alert-danger";
        errorDiv.role = "alert";
        errorDiv.innerHTML = errorText;

        errorContainer.appendChild(errorDiv);
    }

}

let img = `<img src='static/assets/img/${path}.png' alt='' srcset=''>`
vector.innerHTML = img;
message.innerHTML = text
let btn = document.querySelector("body > div.content > button");

btn.addEventListener('click', () => {
    window.location.href = '/';
})

setTimeout(() => {

    //    window.location.href = '/';
}, 1000 * 20);