from models import db, Usuario, Playlist, Musica, MusicaPlaylist


def criar_playlist(usuario_id, nome_playlist):
    """
    Cria uma playlist para um usuário.

    Observação: Playlist é uma entidade fraca com chave composta (playlist_id, usuario_id).
    Aqui o `playlist_id` é gerado automaticamente (autoincrement). O `usuario_id` faz parte
    da chave primária e é uma FK para `Usuario`.
    """
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        raise ValueError('Usuário não encontrado')
    playlist = Playlist(usuario_id=usuario_id, nome=nome_playlist)
    db.session.add(playlist)
    db.session.commit()
    return playlist


def adicionar_musica_playlist(usuario_id, playlist_id, musica_id, ordem_na_playlist):
    """
    Adiciona uma música a uma playlist específica.

    A tabela `MusicaPlaylist` é a tabela associativa (associative table) que representa o
    relacionamento N:N entre `Musica` e `Playlist` e guarda o atributo adicional `ordem_na_playlist`.
    """
    # Verifica existência
    musica = Musica.query.get(musica_id)
    if not musica:
        raise ValueError('Música não encontrada')

    playlist = Playlist.query.filter_by(playlist_id=playlist_id, usuario_id=usuario_id).first()
    if not playlist:
        raise ValueError('Playlist não encontrada')

    # Previne duplicatas na mesma ordem (UniqueConstraint garante no BD)
    existente = MusicaPlaylist.query.filter_by(playlist_id=playlist_id, usuario_id=usuario_id, ordem_na_playlist=ordem_na_playlist).first()
    if existente:
        raise ValueError('Já existe música nesta ordem na playlist')

    mp = MusicaPlaylist(musica_id=musica_id, playlist_id=playlist_id, usuario_id=usuario_id, ordem_na_playlist=ordem_na_playlist)
    db.session.add(mp)
    db.session.commit()
    return mp


def remover_musica_playlist(usuario_id, playlist_id, musica_id):
    """
    Remove uma música de uma playlist específica.
    """
    mp = MusicaPlaylist.query.filter_by(musica_id=musica_id, playlist_id=playlist_id, usuario_id=usuario_id).first()
    if not mp:
        return False
    db.session.delete(mp)
    db.session.commit()
    return True
