from flask import Flask
from config import Config
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Ponto de entrada da aplicação Flask.

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Cria as tabelas ao executar o arquivo.
        db.create_all()
        print('Tabelas criadas (se ainda não existiam).')
    # Inicia servidor Flask para desenvolvimento/execução simples.
    # Em produção com Neon, prefira usar um WSGI server (gunicorn) e variáveis de ambiente.
    app.run(host='0.0.0.0', port=5000)
