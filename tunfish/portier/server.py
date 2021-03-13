from sqlalchemy import exc
from tunfish.portier.model import Network, Gateway, Router, WireGuardNode
from tunfish.portier.database.control import dbc
from tunfish.portier.util import sa_to_dict


class PortierRPC:

    def __init__(self, fabric):
        self.dbc_handler = dbc()
        self.fabric = fabric

    # data json dict
    async def request_gateway(self, data):
        print(f"data: {data}")
        print(f"query gateway")
        gateway = self.dbc_handler.session.query(Gateway).filter_by(active=True).order_by(Gateway.counter).first()
        print(f"Gateway: {gateway}")
        print(f"done.")
        pubkey = await self.fabric.call(u'com.gw.open_interface', data)

        print(f"value task: {pubkey}")

        """
        gw = {
            "ip": gateway.ip,
            "name": gateway.name,
            "wgpubkey": pubkey,
            "listen_port": 42001,
            "endpoint": gateway.ip
        }
        """
        # maybe better way, not tested
        # return gateway.__dict__
        return sa_to_dict(gateway)


    def register_gateway(self, data):
        print(f"register_gateway_data: {data}")
        gateway = self.dbc_handler.session.query(Gateway).filter_by(name=data['name']).first()
        print(f"GATEWAY: {gateway}")
        gateway.active = True
        self.dbc_handler.session.commit()

    def request_status(self):
        print(f"Status: {self.__dict__}")

    def request_node_config(self, node_public_key: str, format=None):
        node = self.dbc_handler.session.query(WireGuardNode).filter(name='public_key').one()
        peers = []
        for n in node.networks:
            net = self.dbc_handler.session.query(Network).filter_by(id=n)
            for p in net.wireguard_nodes:
                peers.append(self.dbc_handler.session.query(WireGuardNode).filter(id=p).one())

        if not format:
            peer_flat_list = []
            for peer in peers:
                peer_flat_list.append(sa_to_dict(peer))
            return (sa_to_dict(node), peer_flat_list)

        elif format == 'qr':
            return self.node_config_to_qr(node=node, peers=peers)

        elif format == 'txt':
            return self.node_config_to_txt(node=node, peers=peers)

    def add_network(self, data):
        print(f"received data from tf-ctl: {data}")
        network = Network(**data)
        print(f"NETWORK: {network}")
        try:
            self.dbc_handler.session.add(network)
            self.dbc_handler.session.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error: {e}")
            self.dbc_handler.session.rollback()
        except Exception as e:
            print(f"{e}")

    def add_gateway(self, data):
        print(f"received data from tf-ctl: {data}")
        network = self.dbc_handler.session.query(Network).filter_by(name=data['network']).first()
        network.gateway.append(Gateway(**data))
        print(f"NETWORK_QUERY:{network.__dict__}")

        try:
            self.dbc_handler.session.add(network)
            self.dbc_handler.session.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error: {e}")
            self.dbc_handler.session.rollback()
        except Exception as e:
            print(f"{e}")

        from tunfish.tools.certificate import Certificate
        cert = Certificate()
        cert.gen_x509(name=data['name'])

    def add_client(self, data):
        print(f"received data from tf-ctl: {data}")
        network = self.dbc_handler.session.query(Network).filter_by(name=data['network']).first()
        network.router.append(Router(**data))
        print(f"NETWORK_QUERY:{network.__dict__}")
        try:
            self.dbc_handler.session.add(network)
            self.dbc_handler.session.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error: {e}")
            self.dbc_handler.session.rollback()
        except Exception as e:
            print(f"{e}")

    def web_get_networks(self):
        network = self.dbc_handler.session.query(Network.name).all()

        print(f"network {network}")

        return network

    def node_config_to_txt(self, node=None, peers=None):
        peers = node.peers

        address_lines = []
        for v in node.addresses:
            line = f"Address = {v}"
            address_lines.append(line)
        addr_txt = "\n".join(address_lines)

        peer_lines = []
        for peer in peers:
            txt = f"""
[Peer]
PublicKey = {peer.public_key} 
AllowedIPs = {", ".join(peer.allowed_ips)} 
Endpoint = {peer.endpoint_addr}:{peer.endpoint_port}
"""
            peer_lines.append(txt)

        peer_txt = "\n".join(peer_lines)

        config_txt = f"""
[Interface]
ListenPort = {node.listen_port} 
PrivateKey = < INSERT PRIVATE KEY HERE > 
{addr_txt}

{peer_txt}
"""
        return config_txt

    def node_config_to_qr(self, node):
        # qrencode -t ansiutf8 < wg-internal.conf
        import qrcode
        data = self.node_config_to_txt(node)
        return qrcode.make(data)

