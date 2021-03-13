#from tunfish.database.control import dbc
#from tunfish.model import Router, Gateway
from sqlalchemy import exc
from tunfish.portier.tools import genwgkeys
from tunfish.portier.database.control import dbc
from tunfish.portier.model import Router, Gateway, WireGuardNode

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

    for i in range(1, 5):
        print(f"NODE: {i}")
        keys = genwgkeys.Keys()
        keys.gen_b64_keys()
        node = WireGuardNode(name=f'Node-{i}',
                             public_key=keys.public_wg_key.decode("utf-8"),
                             endpoint_addr=f'10.147.90.5{i}',
                             endpoint_port=42000 + i,
                             allowed_ips=f'0.0.0.0/0',
                             persistent_keepalive=25)
        db_insert(node)



create_device_fixture()
dbc_handler.session.close()
