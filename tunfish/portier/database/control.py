# db_control.py
from tunfish.portier.database.create_database import create_postgresql_database
from tunfish.portier.database.create_gw_table import create_gw_table
from tunfish.portier.database.create_router_table import create_router_table
from tunfish.portier.database.create_network_table import create_network_table
from tunfish.portier.database.create_node_table import create_node_table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tunfish.portier.model import Base


class dbc:

    db_uri = 'postgresql://tfuser:dbpw@localhost:5432/tunfishdb'
    engine = None
    session = None

    def __init__(self):
        self.create_db_engine()
        self.create_session()
        self.create_db()

    def create_db_engine(self):
        print(f"create_db_engine")
        self.engine = create_engine(self.db_uri)

    def create_session(self):
        print(f"create_session")
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def create_db(self):
        print(f"create_db")
        create_postgresql_database(self.engine)
        #create_network_table(self.engine)
        #create_gw_table(self.engine)
        #create_router_table(self.engine)
        #create_node_table(self.engine)
        #Base = declarative_base()
        Base.metadata.create_all(self.engine)