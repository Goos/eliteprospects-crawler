import os
import logging
from sqlalchemy import * 
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists

Base = declarative_base()
logger = logging.getLogger(__name__) 

class Player(Base):
  __tablename__ = 'players'

  id = Column(Integer, primary_key=True)
  eliteprospects_id = Column(Integer, index=True, unique=True)
  name = Column(String)
  birthdate = Column(DateTime)
  birthplace = Column(String)
  age = Column(Integer)
  nationality = Column(String)
  position = Column(String)
  shooting_direction = Column(String)
  catching_direction = Column(String)
  height = Column(Float)
  weight = Column(Float)
  status = Column(String, default='Active')
  youth_team = Column(String)


class DBClient():
  def __init__(self, host=None, driver=None, dbname=None, username=None, password=None):
    host = host if host else os.environ.get('DATABASE_HOST')
    driver = driver if driver else os.environ.get('DATABASE_DRIVER')
    dbname = dbname if dbname else os.environ.get('DATABASE_NAME')
    username = username if username else os.environ.get('DATABASE_USERNAME')
    password = password if password else os.environ.get('DATABASE_PASSWORD')

    uri = ("%s://%s:%s@%s/%s" % (driver, username, password, host, dbname)).strip()
    
    logger.info("Connecting to database with URI: %s", uri)

    self.engine = create_engine(uri)

    Session = sessionmaker()
    Session.configure(bind=self.engine)
    self.session = Session()

    self.metadata = Base.metadata

    self.metadata.create_all(self.engine)

  def player_exists(self, eliteprospects_id=None, player_id=None):
    stmt = None
    if eliteprospects_id:
      stmt = exists().where(Player.eliteprospects_id == eliteprospects_id)
    elif player_id:
      stmt = exists().where(Player.player_id == player_id)

    return self.session.query(stmt).scalar()

  def add_player(self, player: Player):
    self.session.add(player)
    self.session.commit()
