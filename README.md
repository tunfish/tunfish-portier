# Quickstart

## Create RSA key and get X.509 certificate
```sh
pip install pki-client
pki-client --ca-url=http://127.0.0.1:8000/ --ca-name=RootCA \
           --cacert=cacert.pem --key=portier.key --certificate=portier.pem --profile=client --common-name-prefix=portier
```

## Setup dependencies
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --editable .
```

## Invoke daemon
```sh
TF_X509_CERT=portier.pem TF_X509_KEY=portier.key TF_X509_CACERT=cacert.pem AUTOBAHN_DEMO_ROUTER=wss://127.0.0.1:8080/ws tf-portier
```
