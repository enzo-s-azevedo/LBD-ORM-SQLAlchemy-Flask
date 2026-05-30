from app import create_app
from models import db, Artista, Usuario, Musica, Playlist, MusicaPlaylist
from relacionamento import criar_playlist, adicionar_musica_playlist


def popular():
    app = create_app()
    with app.app_context():
        # Cria as tabelas do projeto.
        db.create_all()

        # Popula ARTISTA.
        artistas_data = [
            ('Queen', 'Britânica'),
            ('Led Zeppelin', 'Britânica'),
            ('AC/DC', 'Australiana'),
            ('Banda X (Pop)', 'Brasileira'),
        ]

        artistas = []
        for nome, nac in artistas_data:
            existente = Artista.query.filter_by(nome=nome).first()
            if existente:
                artistas.append(existente)
            else:
                a = Artista(nome=nome, nacionalidade=nac)
                db.session.add(a)
                db.session.commit()
                artistas.append(a)

        print('Artistas inseridos')

        # Popula USUARIO.
        usuarios_data = [
            ('Pablo', 'pablo@aluno.com'),
            ('Josue', 'josue@aluno.com'),
            ('Alexandre', 'alexandre@aluno.com'),
        ]

        usuarios = []
        for username, email in usuarios_data:
            existente = Usuario.query.filter_by(username=username).first()
            if existente:
                usuarios.append(existente)
            else:
                u = Usuario(username=username, email=email)
                db.session.add(u)
                db.session.commit()
                usuarios.append(u)

        print('Usuários inseridos')

        # Popula MUSICA.
        musicas_data = [
            ('Bohemian Rhapsody', 354, artistas[0].id),
            ('Stairway to Heaven', 482, artistas[1].id),
            ('Back In Black', 255, artistas[2].id),
            ('We Will Rock You', 160, artistas[0].id),
            ('Musica Pop Brasileira', 180, artistas[3].id),
            ('Thunderstruck', 292, artistas[2].id),
        ]

        musicas = []
        for titulo, duracao, artista_id in musicas_data:
            existente = Musica.query.filter_by(titulo=titulo).first()
            if existente:
                musicas.append(existente)
            else:
                m = Musica(titulo=titulo, duracao_segundos=duracao, artista_id=artista_id)
                db.session.add(m)
                db.session.commit()
                musicas.append(m)

        print('Músicas inseridas')

        # Cria a playlist "Sertanejos do Josue" para o usuário Josue.
        josue = Usuario.query.filter_by(username='Josue').first()
        if not josue:
            raise ValueError('Usuário Josue não encontrado')

        sertanejos_do_josue = Playlist.query.filter_by(nome='Sertanejos do Josue', usuario_id=josue.id).first()
        if not sertanejos_do_josue:
            sertanejos_do_josue = criar_playlist(josue.id, 'Sertanejos do Josue')

        # Cria as demais playlists.
        playlists_data = [
            (usuarios[0].id, 'Rock do Pablo'),    # (1,1)
            (usuarios[1].id, 'Baladas do Josue'), # (2,2)
            (usuarios[0].id, 'Heavy Riffs'),      # (3,1)
        ]

        playlists = [sertanejos_do_josue]
        for usuario_id, nome in playlists_data:
            existente = Playlist.query.filter_by(nome=nome, usuario_id=usuario_id).first()
            if existente:
                playlists.append(existente)
            else:
                playlists.append(criar_playlist(usuario_id, nome))

        print('Playlists inseridas')

        # Cria as associações N:N entre músicas e playlists.
        rock = Playlist.query.filter_by(nome='Rock do Pablo', usuario_id=usuarios[0].id).first()
        baladas = Playlist.query.filter_by(nome='Baladas do Josue', usuario_id=usuarios[1].id).first()
        heavy = Playlist.query.filter_by(nome='Heavy Riffs', usuario_id=usuarios[0].id).first()

        relacoes = [
            (musicas[0].id, rock.playlist_id, rock.usuario_id, 1),
            (musicas[2].id, rock.playlist_id, rock.usuario_id, 2),
            (musicas[3].id, rock.playlist_id, rock.usuario_id, 3),
            (musicas[1].id, baladas.playlist_id, baladas.usuario_id, 1),
            (musicas[2].id, heavy.playlist_id, heavy.usuario_id, 1),
            (musicas[5].id, heavy.playlist_id, heavy.usuario_id, 2),
        ]

        for musica_id, playlist_id, usuario_id, ordem in relacoes:
            existente = MusicaPlaylist.query.filter_by(
                musica_id=musica_id,
                playlist_id=playlist_id,
                usuario_id=usuario_id,
                ordem_na_playlist=ordem,
            ).first()
            if existente:
                continue
            adicionar_musica_playlist(usuario_id, playlist_id, musica_id, ordem)

        print('Relacionamentos N:N inseridos')

        # Exemplo de leitura: playlists do Pablo.
        pablo = Usuario.query.filter_by(username='Pablo').first()
        print('\nPlaylists do Pablo:')
        for p in pablo.playlists:
            print(f'- {p.nome} (playlist_id={p.playlist_id}, usuario_id={p.usuario_id})')

        # Exemplo de leitura: músicas da playlist "Rock do Pablo".
        rock = Playlist.query.filter_by(nome='Rock do Pablo', usuario_id=pablo.id).first()
        print('\nMúsicas na playlist "Rock do Pablo":')
        mps = MusicaPlaylist.query.filter_by(playlist_id=rock.playlist_id, usuario_id=rock.usuario_id).order_by(MusicaPlaylist.ordem_na_playlist).all()
        for mp in mps:
            musica = db.session.get(Musica, mp.musica_id)
            artista = db.session.get(Artista, musica.artista_id)
            print(f'ordem {mp.ordem_na_playlist}: {musica.titulo} - artista: {artista.nome}')


if __name__ == '__main__':
    popular()
