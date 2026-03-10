from http.server import BaseHTTPRequestHandler
import json
import requests

def obter_taxas():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/JPY")
    if response.status_code == 200:
        return response.json()['rates']
    else:
        raise Exception("Erro ao obter taxas de câmbio.")

def conversao_yen(valor, moeda_origem, moeda_destino, taxas):
    if moeda_origem in taxas and moeda_destino in taxas:
        taxa_origem = taxas[moeda_origem]
        taxa_destino = taxas[moeda_destino]
        valor_em_yenes = valor / taxa_origem
        valor_convertido = valor_em_yenes * taxa_destino
        return valor_convertido
    else:
        raise ValueError("Conversão não suportada.")

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Permite que o frontend converse com o backend sem ser bloqueado (CORS)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            # Lê os dados enviados pelo site
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            valor = float(data.get('valor', 0))
            peso = float(data.get('peso', 0))

            if valor <= 0:
                 raise ValueError("O valor deve ser maior que zero.")

            # Faz os cálculos
            taxas = obter_taxas()
            valor_convertido = conversao_yen(valor, 'JPY', 'BRL', taxas)
            
            X = valor_convertido * 1.2
            parte1 = peso * 160 / 2000
            parte2 = peso * 300 / 2000
            resultado = X + parte1 + parte2

            # Prepara a resposta
            response_data = {
                "jpy_origin": valor,
                "brl_converted": valor_convertido,
                "final_result": resultado
            }

            # Envia sucesso (200 OK) e os dados
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        except Exception as e:
            # Se der erro, envia aviso de erro mas sem quebrar a conexão
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_data = {"error": str(e)}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
