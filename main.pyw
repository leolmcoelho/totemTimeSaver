import json, os
from flask import Flask, render_template, redirect, request


#from bots import exec

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/index")
def r_home():
    return redirect('/')


@app.route("/video")
def video():
    return render_template('video.html')


@app.route("/result")
def result():
    return render_template('result.html')

@app.route("/teste")
def teste():
    return render_template('teste.html')


@app.route("/amil_token")
def amil():
    return render_template('amil.html')


@app.route("/api/write-token", methods=["GET"])
def write_token():
    token = request.args.get("token") # Obtém o valor do token do parâmetro "token" na URL
    data = {"token": token}
    with open("config/token.json", "w") as f:
        json.dump(data, f)
    return {"code": 200, "message": "Token escrito com sucesso!"}
   
    
@app.route("/api/start-bot", methods=['GET'])
def start_bot():
    #print()
    name = request.args.get('name')
    os.system(f'py bots.pyw "{name}" &')
    #exec(name)
    return {'data': request.args.get('name')}
   

@app.route("/api/status-bot")
def status_bot():
    with open('status.json') as f:
        status_data  = json.loads(f.read())
    
    with open('config/error.json') as f:
        error_data  = json.loads(f.read())
    
    return {**status_data, **error_data}



@app.route("/api/reset-status-bot")
def reset_status_bot():
    with open('status.json', 'w') as f:
        json.dump({"code": 100}, f)
    return {"code": 200, "message": "status resetado com sucesso"}




if __name__ == "__main__":
    leo = True
    if leo:
        print(app.config['TEMPLATES_AUTO_RELOAD'])
    #app.logger.setLevel(logging.ERROR)    
    app.run(debug=True)
    

