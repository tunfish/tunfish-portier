from testfixtures import compare

from tunfish.portier.model import Base, Gateway, Network, Router, WireGuardNode
from tunfish.portier.tools import genwgkeys


def test_connection(connection):
    # Do fancy stuff with the connection.
    # Note you will not need to close the connection. This is done
    # automatically when the scope (module) of the fixtures ends.
    assert connection


def test_entities(engine, dbsession, truncate_db, insert):

    Base.metadata.create_all(engine)

    # 1. Add some entities and verify them.
    for i in range(5, 10):
        keys = genwgkeys.Keys()
        keys.gen_b64_keys()

        router = Router(
            device_id=f"DEV081{i}",
            user_pw=f"userpw{i}",
            device_pw=f"rootpw{i}",
            wgprvkey=keys.private_wg_key.decode("utf-8"),
            wgpubkey=keys.public_wg_key.decode("utf-8"),
            ip=f"10.0.23.1{i}",
        )

        insert(router)

    for i in range(1, 2):
        gateway = Gateway(name="gateone", os="debian10", ip="172.16.42.50")
        insert(gateway)

    for i in range(1, 3):
        network = Network(name=f"network-{i}", subnet=f"10.10.{i}0.0/24")
        insert(network)

    for i in range(1, 5):
        keys = genwgkeys.Keys()
        keys.gen_b64_keys()
        node = WireGuardNode(
            name=f"Node-{i}",
            public_key=keys.public_wg_key.decode("utf-8"),
            addresses=[f"10.10.10.{i}", f"10.10.20.{i}"],
            listenport=42000 + i,
            allowed_ips=f"0.0.0.0/0",
            persistent_keepalive=25,
        )
        insert(node)

    dbsession.commit()

    assert dbsession.query(Router).count() == 5
    assert dbsession.query(Gateway).count() == 1
    assert dbsession.query(Network).count() == 2
    assert dbsession.query(WireGuardNode).count() == 4

    gw1: Gateway = dbsession.query(Gateway).first()
    assert gw1.name == "gateone"
    assert gw1.os == "debian10"
    assert gw1.ip == "172.16.42.50"

    # 2. Add some associations and verify them.
    nw1 = dbsession.query(Network).filter_by(name="network-1").one()
    wn1 = dbsession.query(WireGuardNode).filter_by(name="Node-1").one()
    wn2 = dbsession.query(WireGuardNode).filter_by(name="Node-2").one()

    nw1.wireguardnodes.append(wn1)
    nw1.wireguardnodes.append(wn2)

    dbsession.commit()

    assert len(nw1.wireguardnodes) == 2
    assert wn1 in nw1.wireguardnodes
    assert wn2 in nw1.wireguardnodes

    dbsession.close()


def test_many_to_many(engine, dbsession, truncate_db, insert):

    Base.metadata.create_all(engine)

    keys = genwgkeys.Keys()
    keys.gen_b64_keys()
    nw = Network(
        name=f"network-TEST",
        wireguardnodes=[
            WireGuardNode(
                name=f"Node-50",
                public_key=keys.public_wg_key.decode("utf-8"),
                addresses=[f"10.10.10.50", f"10.10.20.50"],
                listenport=42099,
                allowed_ips=f"0.0.0.0/0",
                persistent_keepalive=25,
            )
        ],
    )
    insert(nw)

    dbsession.commit()

    assert dbsession.query(Network).count() == 1
    assert dbsession.query(WireGuardNode).count() == 1

    network = dbsession.query(Network).one()
    assert network.wireguardnodes[0].addresses == ["10.10.10.50", "10.10.20.50"]

    #wn1: WireGuardNode = network.wireguardnodes[0]
    #compare(wn1, WireGuardNode(name="Node-50"))

    dbsession.close()

def test_one_to_many(engine, dbsession, truncate_db, insert):

    Base.metadata.create_all(engine)

    for i in range(1, 3):
        keys = genwgkeys.Keys()
        keys.gen_b64_keys()
        node = WireGuardNode(
            name=f"Node-{i}",
            public_key=keys.public_wg_key.decode("utf-8"),
            addresses=[f"10.10.10.{i}", f"10.10.20.{i}"],
            listenport=42000 + i,
            allowed_ips=f"0.0.0.0/0",
            persistent_keepalive=25,
        )
        insert(node)

    dbsession.commit()

    keys = genwgkeys.Keys()
    keys.gen_b64_keys()

    node = WireGuardNode(
                name=f"Node-100",
                public_key=keys.public_wg_key.decode("utf-8"),
                addresses=[f"10.10.10.100", f"10.10.20.100"],
                listenport=44000,
                allowed_ips=f"0.0.0.0/0",
                persistent_keepalive=25,
            )
    insert(node)
    dbsession.commit()
    assert dbsession.query(WireGuardNode).count() == 3

    wn1 = dbsession.query(WireGuardNode).filter_by(name="Node-1").one()
    wn2 = dbsession.query(WireGuardNode).filter_by(name="Node-2").one()

    node.peers.append(wn1)
    node.peers.append(wn2)
    #node.peers = [wn1, wn2]
    dbsession.commit()
    assert len(node.peers) == 2
    assert node.peers[0] == wn1
    assert node.peers[1] == wn2
    assert wn1 in node.peers
    assert wn2 in node.peers

    dbsession.close()
