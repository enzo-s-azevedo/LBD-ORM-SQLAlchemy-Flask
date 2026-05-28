# LBD-ORM-SQLAlchemy — Resumo rápido

Propósito
- Projeto de exemplo que demonstra modelagem ORM com SQLAlchemy + Flask para
	um sistema de músicas e playlists (1:N, N:N com tabela associativa, constraints).

Como rodar (rápido)
1) Garanta PostgreSQL local acessível. (Opcional: criar DB e ajustar senha)

```bash
sudo -u postgres psql -c "CREATE DATABASE projeto_orm;" || true
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

2) Preparar ambiente e instalar dependências

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Rodar com um comando (gera tabelas e popula):

```bash
chmod +x run_local.sh
./run_local.sh
```

Ou manualmente:

```bash
python3 popular_bd.py   # popula DB
python3 app.py         # inicia a app
```

Arquivos principais (o que cada `.py` faz)
- `app.py`: cria a app Flask, carrega `Config` e inicializa `db`; ao executar diretamente cria tabelas.
- `config.py`: configura `SQLALCHEMY_DATABASE_URI` (lê `DATABASE_URL` ou usa padrão local).
- `models.py`: declara os modelos `Artista`, `Usuario`, `Musica`, `Playlist`, `MusicaPlaylist` com constraints e relacionamentos.
- `popular_bd.py`: script que cria tabelas, insere dados de exemplo e imprime consultas de demonstração.
- `crud.py`: operações CRUD para `Artista` e `Musica` (criar/ler/atualizar/remover).
- `relacionamento.py`: funções para criar playlists e gerenciar músicas nelas (N:N via `MusicaPlaylist`).

Utilitários
- `run_local.sh`: automatiza criação do DB, venv, instalação, popula e inicia a app (logs em `app.log`).

