# LBD-ORM-SQLAlchemy-Fpaso

Projeto de exemplo que demonstra mapeamento ORM com SQLAlchemy/Flask
para um sistema de músicas e playlists (entidades fortes, entidade fraca,
relação N:N com tabela associativa explícita).

Como funciona (resumo):
- Modelos em `models.py`: `Artista`, `Usuario`, `Musica`, `Playlist` (chave composta)
	e `MusicaPlaylist` (tabela associativa com `ordem_na_playlist`).
- Relacionamentos: 1:N (`Artista`->`Musica`, `Usuario`->`Playlist`) e N:N
	(`Musica`<->`Playlist` via `MusicaPlaylist`).
- Constraints: `PRIMARY KEY`, `UNIQUE`, `CHECK`, `ForeignKeyConstraint` (chave composta),
	`UniqueConstraint` e `cascade` configurados no ORM.

Como usar (rápido):
1. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Configure a conexão com PostgreSQL (opcional):

```bash
export DATABASE_URL='postgresql://usuario:senha@host:porta/nome_bd'
```

Se não definido, a URI padrão é `postgresql://postgres:postgres@localhost:5432/projeto_orm`.

4. Criar tabelas e popular dados de exemplo:

```bash
python3 popular_bd.py
```

5. Iniciar a aplicação (gera tabelas se necessário):

```bash
python3 app.py
```

Principais arquivos:
- `app.py` — cria a app Flask e inicializa o `db`.
- `config.py` — configurações de conexão (SQLALCHEMY_DATABASE_URI).
- `models.py` — mapeamento ORM completo e comentários explicativos.
- `crud.py` — funções CRUD para `Artista` e `Musica`.
- `relacionamento.py` — funções para criar playlists e gerenciar músicas nelas.
- `popular_bd.py` — script de exemplo para criar tabelas e inserir dados.

Observações rápidas:
- A tabela `Playlist` é uma entidade fraca (chave composta `playlist_id, usuario_id`).
- `MusicaPlaylist` é a tabela associativa explícita que guarda o atributo extra
	`ordem_na_playlist` e usa `ForeignKeyConstraint` para referenciar a chave composta.
- O ORM substitui SQL manual ao declarar modelos e relacionamentos; o SQLAlchemy
	gera e executa as instruções necessárias conforme as operações em objetos Python.

Contribuições e dúvidas: abra uma issue ou solicite alterações no README.
