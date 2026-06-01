# LBD-ORM-SQLAlchemy — Conectar ao Neon (resumo rápido)

Propósito
- Projeto de exemplo que demonstra modelagem ORM com SQLAlchemy + Flask para um sistema de músicas e playlists.

Requisitos
- Defina `DATABASE_URL` apontando para seu banco Neon (veja `.env.example`).
- Python 3.8+ e dependências em `requirements.txt`.

Instalação
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Popular com dados de exemplo
```bash
python3 popular_bd.py
```

Executar a aplicação
- Execução simples (desenvolvimento):
```bash
python3 app.py
```
- Em produção, use um WSGI server (por exemplo `gunicorn`) e forneça `DATABASE_URL` via variáveis de ambiente.

Arquivos principais
- `config.py`: carrega `DATABASE_URL` (via `.env` ou env vars) e valida sua presença.
- `app.py`: cria a app Flask e inicializa `db`.
- `models.py`: modelos e relacionamentos.
- `popular_bd.py`: popula o banco com dados de exemplo.
- `validate_neon.py`: script de verificação e sanity-check do banco.

Notebook interativo
- Abra `pipeline.ipynb` e execute as células na ordem para: criar a playlist de exemplo, adicionar a música `Stairway to Heaven` e removê-la. Use Jupyter ou VS Code Notebook.

