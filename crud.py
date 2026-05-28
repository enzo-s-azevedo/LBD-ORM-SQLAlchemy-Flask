from models import db, Artista, Musica


# ARTISTA CRUD
def criar_artista(nome, nacionalidade=None):
    artista = Artista(nome=nome, nacionalidade=nacionalidade)
    db.session.add(artista)
    db.session.commit()
    return artista


def buscar_artista_por_id(artista_id):
    return db.session.get(Artista, artista_id)


def atualizar_artista(artista_id, **kwargs):
    artista = db.session.get(Artista, artista_id)
    if not artista:
        return None
    for key, value in kwargs.items():
        if hasattr(artista, key):
            setattr(artista, key, value)
    db.session.commit()
    return artista


def remover_artista(artista_id):
    artista = db.session.get(Artista, artista_id)
    if not artista:
        return False
    db.session.delete(artista)
    db.session.commit()
    return True


# MUSICA CRUD
def criar_musica(titulo, duracao_segundos, artista_id):
    musica = Musica(titulo=titulo, duracao_segundos=duracao_segundos, artista_id=artista_id)
    db.session.add(musica)
    db.session.commit()
    return musica


def buscar_musica_por_id(musica_id):
    return db.session.get(Musica, musica_id)


def atualizar_musica(musica_id, **kwargs):
    musica = db.session.get(Musica, musica_id)
    if not musica:
        return None
    for key, value in kwargs.items():
        if hasattr(musica, key):
            setattr(musica, key, value)
    db.session.commit()
    return musica


def remover_musica(musica_id):
    musica = db.session.get(Musica, musica_id)
    if not musica:
        return False
    db.session.delete(musica)
    db.session.commit()
    return True
