# create_node_table.py
from tunfish.portier.model import WireGuardNode


def create_node_table(engine):
    WireGuardNode.__table__.create(bind=engine, checkfirst=True)
