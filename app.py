from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    # Lê o texto inserido no formulário pleo usuário
    original_text = request.form['text']
    target_language = request.form['language']

    # Carrega os valores de .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Cria o caminho para chamar a API
    path = '/translate?api-version=3.0'
    # Adiciona o parâmetro do idioma desejado
    target_language_parameter = '&to=' + target_language
    # Cria a URL completa
    constructed_url = endpoint + path + target_language_parameter

    # Configura as informações da header, que inclue a chave de assinatura
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Cria o corpo da solicitação com o texto a ser traduzido
    body = [{ 'text': original_text }]

    # Chama o serviço de tradução com POST request
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Recupera a resposta em JSON
    translator_response = translator_request.json()
    # Recupera a tradução
    translated_text = translator_response[0]['translations'][0]['text']

    # Chama render templatepara exibir a página de resposta
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )