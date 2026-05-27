from app import create_app
from models import db, Artista, Usuario
import crud
import relacionamento


def popular():
    app = create_app()
    with app.app_context():
        # Cria todas as tabelas (se ainda não existirem)
        db.create_all()

        # Limpa tabelas para execução repetida (apenas para script de demonstração)
        db.session.query(Artista).delete()
        db.session.query(Usuario).delete()
        db.session.commit()

        # Inserir dados iniciais
        a1 = crud.criar_artista('The Example Band', 'Brasil')
        a2 = crud.criar_artista('Singer Solo', 'Portugal')

        u1 = Usuario(username='alice', email='alice@example.com')
        u2 = Usuario(username='bob', email='bob@example.com')
        db.session.add_all([u1, u2])
        db.session.commit()

        m1 = crud.criar_musica('Primeira Faixa', 210, a1.id)
        m2 = crud.criar_musica('Segunda Faixa', 185, a2.id)
        m3 = crud.criar_musica('Terceira Faixa', 200, a1.id)

        # Criar playlist para Alice
        p1 = relacionamento.criar_playlist(u1.id, 'Playlist da Alice')

        # Adicionar músicas em ordens
        relacionamento.adicionar_musica_playlist(u1.id, p1.playlist_id, m1.id, 1)
        relacionamento.adicionar_musica_playlist(u1.id, p1.playlist_id, m2.id, 2)

        # Testar remoção
        relacionamento.remover_musica_playlist(u1.id, p1.playlist_id, m2.id)

        # Mostrar resumos
        print('Artistas:', Artista.query.all())
        print('Usuarios:', Usuario.query.all())
        print('Playlists de Alice:', [p for p in u1.playlists])


if __name__ == '__main__':
    popular()
