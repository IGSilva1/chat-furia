import os
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    user_message = data.get('message', '')
    reply = generate_reply(user_message)
    return jsonify({'reply': reply})

def generate_reply(message):
    message = message.lower()
    
    if "jogo" in message:
        return "O próximo jogo da FURIA será no sábado às 16h contra a Team Liquid."
    elif "placar" in message:
        return "O último jogo terminou com vitória da FURIA por 2 a 1 contra a paiN."
    elif "furia" in message:
        return "A FURIA é uma das principais organizações de eSports do Brasil, com destaque no CS:GO."
    elif "elenco" in message or "escalação" in message or "jogadores" in message:
        return "O elenco atual da FURIA no CS:GO conta com arT, KSCERATO, yuurih, chelo e FalleN."
    elif "campeonato" in message or "torneio" in message or "próximo torneio" in message:
        return "A FURIA está se preparando para disputar o IEM Dallas no final do mês."
    elif "história" in message or "fundação" in message:
        return "A FURIA foi fundada em 2017 e rapidamente se destacou no cenário competitivo de CS:GO."
    elif "twitter" in message or "redes sociais" in message or "instagram" in message:
        return "Você pode seguir a FURIA no Twitter (@FURIA) e no Instagram (@furia) para atualizações em tempo real."
    elif "curiosidade" in message or "sabia que" in message:
        return "Sabia que a FURIA foi a primeira equipe brasileira a vencer um evento Tier S na América do Norte?"
    elif "notícia" in message or "últimas notícias" in message:
        return "Confira as últimas notícias da FURIA no site oficial ou nas redes sociais!"
    else:
        return "Desculpe, não entendi. Pode reformular sua pergunta?"


def enviar_notificacoes_jogo():
    import time
    while True:
        socketio.emit('game_update', {'message': '⚠️ A FURIA acaba de vencer o primeiro mapa!'})
        time.sleep(60)

if __name__ == '__main__':
    socketio.start_background_task(enviar_notificacoes_jogo)
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
