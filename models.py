from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint, ForeignKeyConstraint

db = SQLAlchemy()


class Artista(db.Model):
    __tablename__ = 'artista'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False, unique=True)
    nacionalidade = db.Column(db.String(100))

    # Relacionamento 1:N: um artista tem muitas músicas
    musicas = db.relationship('Musica', back_populates='artista', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Artista {self.nome}>"


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)

    # Relacionamento 1:N: um usuário tem muitas playlists
    playlists = db.relationship('Playlist', back_populates='usuario', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Usuario {self.username}>"


# Entidade fraca: PLAYLIST depende de USUARIO; chave primária composta (playlist_id, usuario_id)
class Playlist(db.Model):
    __tablename__ = 'playlist'

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # relacionamento many-to-one: muitas playlists pertencem a um usuário (1:N)
    usuario = db.relationship('Usuario', back_populates='playlists')

    # Associação com músicas via tabela associativa explícita (MusicaPlaylist)
    musica_playlists = db.relationship('MusicaPlaylist', back_populates='playlist', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Playlist {self.nome} ({self.playlist_id},{self.usuario_id})>"


class Musica(db.Model):
    __tablename__ = 'musica'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    duracao_segundos = db.Column(db.Integer, nullable=False)
    artista_id = db.Column(db.Integer, db.ForeignKey('artista.id', ondelete='RESTRICT'), nullable=False)

    __table_args__ = (
        CheckConstraint('duracao_segundos > 0', name='ck_duracao_positive'),
    )

    # relacionamento many-to-one: muitas músicas pertencem a um artista (1:N)
    artista = db.relationship('Artista', back_populates='musicas')

    # Associação com playlists via tabela associativa explícita (MusicaPlaylist)
    musica_playlists = db.relationship('MusicaPlaylist', back_populates='musica', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Musica {self.titulo}>"


class MusicaPlaylist(db.Model):
    __tablename__ = 'musica_playlist'

    musica_id = db.Column(db.Integer, db.ForeignKey('musica.id', ondelete='CASCADE'), primary_key=True)
    playlist_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, primary_key=True)
    ordem_na_playlist = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        # ForeignKeyConstraint referenciando a chave composta da tabela Playlist
        ForeignKeyConstraint(['playlist_id', 'usuario_id'], ['playlist.playlist_id', 'playlist.usuario_id'], ondelete='CASCADE'),
        UniqueConstraint('playlist_id', 'usuario_id', 'ordem_na_playlist', name='uq_playlist_ordem'),
    )

    # Relacionamentos de navegação
    musica = db.relationship('Musica', back_populates='musica_playlists')
    playlist = db.relationship('Playlist', back_populates='musica_playlists')

    def __repr__(self):
        return f"<MusicaPlaylist musica={self.musica_id} playlist=({self.playlist_id},{self.usuario_id}) ordem={self.ordem_na_playlist}>"

    # Nota: esta é a tabela associativa explícita para o relacionamento N:N entre Musica e Playlist.
    # Cada registro representa a presença de uma música numa playlist específica e guarda o atributo
    # adicional `ordem_na_playlist`.
