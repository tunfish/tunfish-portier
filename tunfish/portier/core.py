from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from tunfish.portier.server import PortierRPC
from tunfish.portier.util import read_config

class Component(ApplicationSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.srv_procedures = PortierRPC(self)

    async def onJoin(self, details):
        # data json dict

        await self.register(self.srv_procedures.request_gateway, u'com.portier.request_gateway')
        print("Registered com.portier.request_gateway")

        await self.register(self.srv_procedures.register_gateway, u'com.portier.register_gateway')
        print("Registered com.portier.register_gateway")

        await self.register(self.srv_procedures.request_status, u'com.portier.request_status')
        print("Registered com.portier.reguest_status")

        await self.register(self.srv_procedures.request_node_config, u'com.portier.request_node_config')
        print("Registered com.portier.request_node_config")

        await self.register(self.srv_procedures.add_network, u'com.portier.add_network')
        print("Registered com.portier.add_network")

        await self.register(self.srv_procedures.add_gateway, u'com.portier.add_gateway')
        print("Registered com.portier.add_gateway")

        await self.register(self.srv_procedures.add_client, u'com.portier.add_client')
        print("Registered com.portier.add_client")

        await self.register(self.srv_procedures.web_get_networks, u'com.portier.get_networks')
        print("Registered com.portier.get_networks")

        self.publish('com.topic.portier.status', "online")


class PortierServer:
    def start(self):
        import six
        import ssl
        # TLS
        # Setup server

        read_config()

        cf = environ.get('TF_X509_CERT', "portier.pem")
        kf = environ.get('TF_X509_KEY', 'portier.key')
        caf = environ.get('TF_X509_CACERT', 'cacert.pem')
        url = environ.get("BROKER_URL", "wss://172.16.42.2:8080/ws")

        server_ctx = ssl.SSLContext()

        server_ctx.verify_mode = ssl.CERT_REQUIRED
        server_ctx.check_hostname = False

        server_ctx.options |= ssl.OP_SINGLE_ECDH_USE
        server_ctx.options |= ssl.OP_NO_COMPRESSION
        server_ctx.load_cert_chain(certfile=cf, keyfile=kf)
        server_ctx.load_verify_locations(cafile=caf)
        server_ctx.set_ciphers('ECDH+AESGCM')

        # url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://127.0.0.1:8080/ws")
        print(f"URL: {url}")
        if six.PY2 and type(url) == six.binary_type:
            url = url.decode('utf8')
        realm = u"tf_cb_router"
        runner = ApplicationRunner(url, realm, ssl=server_ctx)
        runner.run(Component)

def start():
    server = PortierServer()
    server.start()
