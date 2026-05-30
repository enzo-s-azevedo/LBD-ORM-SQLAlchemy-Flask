from models import db, Usuario, Playlist, Musica, MusicaPlaylist
from sqlalchemy import func


def criar_playlist(usuario_id, nome_playlist):
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        raise ValueError('Usuário não encontrado')
    playlist = Playlist(usuario_id=usuario_id, nome=nome_playlist)
    db.session.add(playlist)
    db.session.commit()
    return playlist


def adicionar_musica_playlist(usuario_id, playlist_id, musica_id, ordem_na_playlist=None):
    musica = db.session.get(Musica, musica_id)
    if not musica:
        raise ValueError('Música não encontrada')

    playlist = Playlist.query.filter_by(playlist_id=playlist_id, usuario_id=usuario_id).first()

    if not playlist:
        raise ValueError('Playlist não encontrada')

    if ordem_na_playlist is None:
        ultima_ordem = db.session.query(
            func.max(MusicaPlaylist.ordem_na_playlist)
        ).filter_by(
            playlist_id=playlist_id,
            usuario_id=usuario_id
        ).scalar()

        ordem_na_playlist = (ultima_ordem or 0) + 1

    else:
        existente = MusicaPlaylist.query.filter_by(playlist_id=playlist_id, usuario_id=usuario_id, 
                                                   ordem_na_playlist=ordem_na_playlist).first()

        if existente:
            raise ValueError('Já existe música nesta ordem na playlist')

    mp = MusicaPlaylist(musica_id=musica_id, playlist_id=playlist_id, usuario_id=usuario_id, ordem_na_playlist=ordem_na_playlist)

    db.session.add(mp)
    db.session.commit()

    return mp


def remover_musica_playlist(usuario_id, playlist_id, musica_id):
    mp = MusicaPlaylist.query.filter_by(musica_id=musica_id, playlist_id=playlist_id, usuario_id=usuario_id).first()
    if not mp:
        return False
    db.session.delete(mp)
    db.session.commit()
    return True
