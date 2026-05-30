from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint, ForeignKeyConstraint

db = SQLAlchemy()


# ARTISTA: entidade forte com PK simples e UNIQUE em nome.
class Artista(db.Model):
    __tablename__ = 'artista'

    id = db.Column(db.Integer, primary_key=True) # PK contém SERIAL (autoincrement=True) por padrão
    nome = db.Column(db.String(255), nullable=False, unique=True) # unique=True = UNIQUE, nullable=False = NOT NULL
    nacionalidade = db.Column(db.String(100))

    # relationship sem presença de FK, representa o lado "1" do relacionamento 1:N com MUSICA
    musicas = db.relationship('Musica', back_populates='artista', cascade='all, delete-orphan') # relationship para navegar entre objetos
    def __repr__(self):
        return f"<Artista {self.nome}>" # Representação textual do objeto


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True) # PK contém SERIAL (autoincrement=True) por padrão
    username = db.Column(db.String(100), nullable=False, unique=True) # unique=True = UNIQUE, nullable=False = NOT NULL
    email = db.Column(db.String(255), nullable=False, unique=True) 

    # relationship sem presença de FK, representa o lado "1" do relacionamento 1:N com PLAYLIST
    playlists = db.relationship('Playlist', back_populates='usuario', cascade='all, delete-orphan') # relationship para navegar entre objetos

    def __repr__(self): 
        return f"<Usuario {self.username}>" # Representação textual do objeto


# PLAYLIST: entidade fraca com PK composta por playlist_id e usuario_id.
class Playlist(db.Model):
    __tablename__ = 'playlist'

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # PK contém SERIAL (autoincrement=True) por padrão
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), primary_key=True) 
    nome = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime(timezone=True),default=lambda: datetime.now(timezone.utc)
)

    # relationship para navegar entre objetos, representa o lado "1" do relacionamento 1:N com USUÁRIO
    usuario = db.relationship('Usuario', back_populates='playlists')

    # Navegação para a tabela N:N com MUSICA.
    musica_playlists = db.relationship('MusicaPlaylist', back_populates='playlist', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Playlist {self.nome} ({self.playlist_id},{self.usuario_id})>"


 # MUSICA: entidade forte com PK simples, NOT NULL e CHECK na duração.
class Musica(db.Model):
    __tablename__ = 'musica'

    id = db.Column(db.Integer, primary_key=True) # PK contém SERIAL (autoincrement=True) por padrão
    titulo = db.Column(db.String(255), nullable=False) # nullable=False = NOT NULL
    duracao_segundos = db.Column(db.Integer, nullable=False) # nullable=False = NOT NULL
    artista_id = db.Column(db.Integer, db.ForeignKey('artista.id', ondelete='RESTRICT'), nullable=False) # ondelete='RESTRICT' impede 
                                                                                                        # exclusão do pai se houver filhos

    __table_args__ = (
        CheckConstraint('duracao_segundos > 0', name='ck_duracao_positive'), # CheckConstraint = CHECK
    )
    # relationship para navegar entre objetos, representa o lado "N" do relacionamento 1:N com ARTISTA (PK)
    artista = db.relationship('Artista', back_populates='musicas') #
    
    #relationship para navegar entre objetos, representa o lado "N" do relacionamento N:N com PLAYLIST (PK composta)
    musica_playlists = db.relationship('MusicaPlaylist', back_populates='musica', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Musica {self.titulo}>" # Representação textual do objeto


# MUSICA_PLAYLIST: tabela de junção do relacionamento N:N.
class MusicaPlaylist(db.Model):
    __tablename__ = 'musica_playlist'

    musica_id = db.Column(db.Integer, db.ForeignKey('musica.id', ondelete='CASCADE'), primary_key=True)
    playlist_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, primary_key=True)
    ordem_na_playlist = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        # FK composta para PLAYLIST.
        ForeignKeyConstraint(['playlist_id', 'usuario_id'], ['playlist.playlist_id', 'playlist.usuario_id'], ondelete='CASCADE'),
        # Uma ordem só pode existir uma vez por playlist.
        UniqueConstraint('playlist_id', 'usuario_id', 'ordem_na_playlist', name='uq_playlist_ordem'),
    )

    # Navegação para MUSICA.
    musica = db.relationship('Musica', back_populates='musica_playlists')
    # Navegação para PLAYLIST.
    playlist = db.relationship('Playlist', back_populates='musica_playlists')

    def __repr__(self):
        return f"<MusicaPlaylist musica={self.musica_id} playlist=({self.playlist_id},{self.usuario_id}) ordem={self.ordem_na_playlist}>"


