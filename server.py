import spacy
import es_core_news_sm
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Cargar el modelo de lenguaje de SpaCy en español
nlp = spacy.load("es_core_news_sm")

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')  # Permitir acceso desde cualquier origen
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if 'text' in data:
            print(data)
            text = data['text']
            encontrada = False
            
            # doc = nlp(text)
            # cadena_a_buscar = data['answer']

            # if cadena_a_buscar in nlp.vocab:
                # encontrada = True
            # for token in doc:
                # if token.text.lower() == cadena_a_buscar.lower():  # Ignora mayúsculas y minúsculas
                    # encontrada = True
                    # break

            response_data = {'encontrada': encontrada}
            self._set_response()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        else:
            self._set_response(status_code=400)
            self.wfile.write('Bad Request - Missing "text" in the request data'.encode('utf-8'))

def run_server(port=8000):
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
