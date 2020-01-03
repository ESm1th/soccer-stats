from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
) 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# from soccer_stats.settings import (
#     POSTGRES_USER,
#     POSTGRES_PASSWORD,
#     POSTGRES_DB
# )
import os
from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB = os.environ['POSTGRES_DB']

engine = create_engine(
    'postgresql+psycopg2://{user}:{password}@localhost/{database}'.format(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB
    )
)


Base = declarative_base()


class Country(Base):
    __tablename__ = 'countries'

    id = Column('id', String, primary_key=True)
    title = Column('title', String, unique=True)

    # relationships
    leagues = relationship('League')


class League(Base):
    __tablename__ = 'leagues'
    
    id = Column(String, primary_key=True)
    title = Column(String, unique=True)
    country_id = Column(String, ForeignKey('countries.id'))
    teams_count = Column(Integer)
    season_start = Column(Integer)
    season_end = Column(Integer)
    all_matches_count = Column(Integer)
    completed = Column(Boolean, default=False)
    image_url = Column(String)
    blocked = Column(Boolean, default=False)

    # relationships
    country = relationship('Country', back_populates='leagues')
    matches = relationship('Match')


class Match(Base):
    __tablename__ = 'matches'

    id = Column(String, primary_key=True)
    league_id = Column(String, ForeignKey('leagues.id'))
    timestamp = Column(Integer)
    home_team = Column(String)
    away_team = Column(String)
    stadium = Column(String)
    home_result = Column(Integer)
    away_result = Column(Integer)
    home_image = Column(String)
    away_image = Column(String)

    # relationships
    league = relationship('League', back_populates='matches')
    statistics = relationship(
        'MatchStatistics',
        uselist=False,
        back_populates='match'
    )


class MatchStatistics(Base):
    __tablename__ = 'statistics'

    id = Column(String, primary_key=True)
    match_id = Column(String, ForeignKey('matches.id'))
    possession_home = Column(Integer)
    possession_away = Column(Integer)
    shots_home = Column(Integer)
    shots_away = Column(Integer)
    cards_home = Column(Integer)
    cards_away = Column(Integer)
    fouls_home = Column(Integer)
    fouls_away = Column(Integer)
    offsides_home = Column(Integer)
    offsides_away = Column(Integer)

    # relationships
    match = relationship('Match', back_populates='statistics')


Base.metadata.create_all(engine)


if __name__ == '__main__':
    print(Country.__table__)