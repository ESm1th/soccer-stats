from contextlib import AbstractContextManager

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from soccer_stats.settings import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB
)


engine = create_engine(
    'postgresql+psycopg2://{user}:{password}@db/{database}'.format(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB
    )
)


Session = sessionmaker(bind=engine)
Base = declarative_base()


class SessionScope(AbstractContextManager):
    def __init__(self, *args, **kwargs):
        self.session = Session()

    def __enter__(self):
        return self.session
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            self.session.rollback()
        self.session.close()


class Country(Base):
    __tablename__ = 'countries'

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, unique=True)

    # relationships
    leagues = relationship('League')


class League(Base):
    __tablename__ = 'leagues'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String)
    country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'))
    teams_count = Column(Integer)
    season_start = Column(Integer)
    season_end = Column(Integer)
    all_matches_count = Column(Integer)
    image_url = Column(String)
    blocked = Column(Boolean, default=False)

    # relationships
    country = relationship('Country', back_populates='leagues')
    matches = relationship('Match')


class Match(Base):
    __tablename__ = 'matches'

    id = Column(UUID(as_uuid=True), primary_key=True)
    league_id = Column(UUID(as_uuid=True), ForeignKey('leagues.id'))
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

    id = Column(UUID(as_uuid=True), primary_key=True)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id'))
    possession_home = Column(Integer)
    possession_away = Column(Integer)
    shots_home = Column(Integer)
    shots_away = Column(Integer)
    cards_home = Column(Integer)
    cards_away = Column(Integer)
    corners_home = Column(Integer)
    corners_away = Column(Integer)
    fouls_home = Column(Integer)
    fouls_away = Column(Integer)
    offsides_home = Column(Integer)
    offsides_away = Column(Integer)

    # relationships
    match = relationship('Match', back_populates='statistics')


Base.metadata.create_all(engine)
