from sqlalchemy import (ARRAY, Boolean, Column, Date, ForeignKey, Integer,
                        Sequence, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

Base = declarative_base()


association_table = Table('association', Base.metadata,
    Column('network_id', Integer, ForeignKey('network.id')),
    Column('wireguardnode_id', Integer, ForeignKey('wireguardnode.id'))
)


class Router(Base):

    __tablename__ = 'router'

    id = Column(Integer, Sequence('tf_id_seq'), primary_key=True)
    device_id = Column('device_id', String(32), unique=True, default=None)
    ip = Column('ip', String(32), default=None)
    device_pw = Column('device_pw', String(32), default=None)
    user_pw = Column('user_pw', String(32), default=None)
    wgprvkey = Column('wgprvkey', String(44), default=None)
    wgpubkey = Column('wgpubkey', String(44), default=None)
    doa = Column('doa', Date, default=None)
    dod = Column('dod', Date, default=None)
    hw_model = Column('hw_model', String(32), default=None)
    hw_version = Column('hw_version', String(32), default=None)
    sw_version = Column('sw_version', String(32), default=None)
    blocked = Column('blocked', Boolean, default=False)

    network_id = Column(Integer, ForeignKey('network.id'))
    network = relationship("Network", back_populates="router")

    gateway_id = Column(Integer, ForeignKey('gateway.id'))
    gateway = relationship("Gateway", back_populates="router")

    # config for wg interface
    listenport = Column('listenport', Integer, default=42001)
    endpoint = Column('endpoint', String(32), default=None)
    allowed_ips = Column('allowed_ips', String(32), default='0.0.0.0/0')

    def __repr__(self):
        return "\ndevice_id='%s', \nip='%s', \ndevice_pw='%s', \nuser_pw='%s', \nwgprvkey='%s', \nwgpubkey='%s'," \
               "\ndoa='%s', \ndod='%s', \nhw_model='%s', \nhw_version='%s', \nsw_version='%s', \nblocked='%s'," \
               "\ngateway='%s', \nlistenport='%s', \nendpoint='%s', \nallowed_ips='%s'" % (
            self.device_id, self.ip, self.device_pw, self.user_pw, self.wgprvkey, self.wgpubkey, self.doa, self.dod,
            self.hw_model, self.hw_version, self.sw_version, self.blocked, self.gateway, self.listenport,
            self.endpoint, self.allowed_ips)


class Gateway(Base):

    __tablename__ = 'gateway'

    id = Column(Integer, Sequence('gw_id_seq'), primary_key=True)
    name = Column('name', String(32), unique=True)
    os = Column('os', String(32), default=None)
    ip = Column('ip', String(32), unique=True)
    host = Column('host', String(32), default=None)
    domain = Column('domain', String(32), default=None)
    tld = Column('tld', String(32), default=None)
    active = Column('active', Boolean, default=False)
    counter = Column('counter', Integer, default=0)

    router = relationship("Router", back_populates='gateway')

    network_id = Column(Integer, ForeignKey('network.id'))
    network = relationship("Network", back_populates="gateway")

    def __repr__(self):
        return "name='%s', os='%s', ip='%s', host='%s', domain='%s', tld='%s', router='%s'" % (
                                self.name, self.os, self.ip, self.host, self.domain, self.tld, self.router)


class Network(Base):

    __tablename__ = 'network'

    id = Column(Integer, Sequence('nw_id_seq'), primary_key=True)
    name = Column('name', String(32), unique=True)
    enabled = Column('enabled', Boolean, default=False)
    subnet = Column('subnet', String(32), unique=True)
    gateway = relationship("Gateway", back_populates='network')
    router = relationship("Router", back_populates='network')

    wireguardnodes = relationship("WireGuardNode", secondary=association_table, back_populates="networks")

    def __repr__(self):
        return "name='%s', enabled='%s'" % (self.name, self.enabled)


class WireGuardNode(Base):

    __tablename__ = 'wireguardnode'

    id = Column(Integer, Sequence('node_id_seq'), primary_key=True)
    name = Column('name', String(32), unique=True)
    public_key = Column('public_key', String(44), unique=True, default=None)
    addresses = Column('addresses', ARRAY(String(32)), unique=True, default=None)
    listenport = Column('listenport', Integer, default=None)
    endpoint_addr = Column('endpoint_addr', String(32), default=None)
    endpoint_port = Column('endpoint_port', Integer, default=None)
    allowed_ips = Column('allowed_ips', String(32), default='0.0.0.0/0')
    persistent_keepalive = Column('persistent_keepalive', Integer, default=25)

    networks = relationship("Network", secondary=association_table, back_populates="wireguardnodes")
