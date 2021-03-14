#from tunfish.database.control import dbc
#from tunfish.model import Router, Gateway
from sqlalchemy import exc
from tunfish.portier.tools import genwgkeys
from tunfish.portier.database.control import dbc
from tunfish.portier.model import Router, Gateway, WireGuardNodes, Network


dbc_handler = dbc()


def create_device_fixture():

    def db_insert(table):
        try:
            dbc_handler.session.add(table)
            dbc_handler.session.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error: {e}")
            dbc_handler.session.rollback()
        except Exception as e:
            print(f"{e}")

    for i in range(5, 10):
        print(f"ROUTER: {i}")

        keys = genwgkeys.Keys()
        keys.gen_b64_keys()

        router = Router(device_id=f'DEV081{i}',
                        user_pw=f'userpw{i}',
                        device_pw=f'rootpw{i}',
                        wgprvkey=keys.private_wg_key.decode("utf-8"),
                        wgpubkey=keys.public_wg_key.decode("utf-8"),
                        ip=f'10.0.23.1{i}')

        db_insert(router)

    for i in range(1, 2):
        print(f"GATEWAY: {i}")
        gateway = Gateway(name='gateone', os='debian10', ip='172.16.42.50')
        db_insert(gateway)

    for i in range(1, 3):
        print(f"NETWORK: {i}")
        network = Network(name=f'network-{i}',
                          subnet=f'10.10.{i}0.0/24')
        db_insert(network)


    for i in range(1, 5):
        print(f"NODE: {i}")
        keys = genwgkeys.Keys()
        keys.gen_b64_keys()
        node = WireGuardNodes(name=f'Node-{i}',
                             public_key=keys.public_wg_key.decode("utf-8"),
                             addresses=[f'10.10.10.{i}', f'10.10.20.{i}'],
                             listenport=42000 + i,
                             allowed_ips=f'0.0.0.0/0',
                             persistent_keepalive=25,)
        db_insert(node)

    keys = genwgkeys.Keys()
    keys.gen_b64_keys()
    nw = Network(name=f'network-TEST', wireguardnodes=[WireGuardNodes(name=f'Node-50',
                             public_key=keys.public_wg_key.decode("utf-8"),
                             addresses=[f'10.10.10.50', f'10.10.20.50'],
                             listenport=42099,
                             allowed_ips=f'0.0.0.0/0',
                             persistent_keepalive=25,)])
    db_insert(nw)
    wn1 = dbc_handler.session.query(WireGuardNodes).filter_by(name='Node-1').one()
    wn2 = dbc_handler.session.query(WireGuardNodes).filter_by(name='Node-2').one()
    nw1 = dbc_handler.session.query(Network).filter_by(name='network-1').one()
    nw1.wireguardnodes.append(wn1)
    nw1.wireguardnodes.append(wn2)
    dbc_handler.session.commit()

create_device_fixture()
dbc_handler.session.close()
