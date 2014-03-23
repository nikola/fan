# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

from sqlalchemy import Table, Column, Integer, String, Unicode, ForeignKey
from sqlalchemy.orm import relation
from models import Base


GenreTranslations = Table(
    "GenreTranslations", Base.metadata,
    Column("TranslationId", Integer, ForeignKey("genres.id")),
    Column("GenreId", Integer, ForeignKey("genres.id")),
)

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    idTmdb = Column(Integer)
    locale = Column(String)
    text = Column(Unicode)
    translations = relation(
        "Genre", secondary=GenreTranslations,
        primaryjoin=GenreTranslations.c.GenreId == id,
        secondaryjoin=GenreTranslations.c.TranslationId == id,
        backref="snoitalsnart",
    )

    def __init__(self):
        pass

    def __repr__(self):
        return "<Genre('%s')>" % (self.id)
