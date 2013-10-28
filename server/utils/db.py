# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import os
from contextlib import contextmanager
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.win32 import getAppStoragePathname
from models import Base

def _getSqliteDsn():
    """
    """
    directory = getAppStoragePathname("ka-boom", "Generic Company")

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = "sqlite:///" + (directory + "\\data").replace("\\", r"\\\\")

    return filename


class StreamManager(object):
    """
    """
    @contextmanager
    def _session(self, session=None):
        """
        """
        if session:
            yield session
        else:
            session = self.session_factory()
            try:
                yield session
            except:
                session.rollback()
                raise
            else:
                session.commit()

    def __init__(self):
        """
        """
        self.engine = create_engine(_getSqliteDsn(), echo=False, module=sqlite)
        self.engine.execute("select 1").scalar()
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.drop_all(self.engine, checkfirst=True)
        Base.metadata.create_all(self.engine)

    def _foo(self):
        """
        """
        with self._session() as session:
            pass
