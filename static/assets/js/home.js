let btn = document.getElementById('btn');
async function main(){
    let url = await fetch('/api/reset-status-bot').then(T => T.json()); 
    console.log(url);
}


btn.onclick = async function() {
    let name = document.querySelector('#name').value;
    localStorage.clear();
    localStorage.setItem('name', name);
    /*console.log('vai fazer a request');
    fetch('api/start-bot?name=' + name).then(T => T.json()); 
    console.log('vai redirecionar');*/
    window.location.href = '/video';
    
}

 main();