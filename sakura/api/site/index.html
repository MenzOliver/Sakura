from http.server import BaseHTTPRequestHandler
import json
import requests

# --- Funções do seu código original (adaptadas) ---
def obter_taxas():
    # Usando a mesma API do seu exemplo
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

# --- Manipulador de Requisições Serverless da Vercel ---
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Configurar cabeçalhos de resposta para JSON
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Adicionar cabeçalhos CORS para permitir chamadas do frontend
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        try:
            # Ler o corpo da requisição
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            # Obter valores do formulário
            valor = float(data.get('valor', 0))
            peso = float(data.get('peso', 0))

            # --- Executar a lógica do seu código original ---
            taxas = obter_taxas()
            
            if valor <= 0:
                 raise ValueError("O valor deve ser maior que zero.")

            valor_convertido = conversao_yen(valor, 'JPY', 'BRL', taxas)
            
            # Multiplicação por 1,2
            X = valor_convertido * 1.2

            # Cálculo das parcelas relacionadas ao peso
            parte1 = peso * 160 / 2000
            parte2 = peso * 300 / 2000

            # Soma final
            resultado = X + parte1 + parte2

            # --- Preparar resposta JSON ---
            response_data = {
                "jpy_origin": valor,
                "brl_converted": valor_convertido,
                "final_result": resultado
            }

            # Enviar resposta JSON
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        except Exception as e:
            # Lidar com erros e retornar uma mensagem clara
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {"error": str(e)}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))

    def do_OPTIONS(self):
        # Responder a requisições preflight CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
