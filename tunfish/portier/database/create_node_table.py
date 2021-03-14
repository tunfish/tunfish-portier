# create_node_table.py
from tunfish.portier.model import WireGuardNodes


def create_node_table(engine):
    WireGuardNodes.__table__.create(bind=engine, checkfirst=True)
