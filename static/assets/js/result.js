
let item = localStorage.getItem('status-bot'),
message = document.querySelector('.message'),
vector = document.querySelector('.vector');


if (item == 200)  {
    var text = 'Atendimento concluído com sucesso!<br>Aguarde ser chamado(a) para sua consulta.'
 
    var path = 'Vector_true';
}
else {
    text ='Erro no processamento. Por favor, dirija-se a recepção.'
    'Erro no processamento. Por favor, dirija-se a recepção.'
    var path = 'Vector';
}

let img =  `<img src='static/assets/img/${path}.png' alt='' srcset=''>`
vector.innerHTML = img;
message.innerHTML = text

setTimeout(() => {

    window.location.href = '/';
}, 1000*20);