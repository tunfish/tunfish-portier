![](https://github.com/tunfish/tunfish-portier/workflows/Tests/badge.svg)
![](https://codecov.io/gh/tunfish/tunfish-portier/branch/main/graph/badge.svg)

# Tunfish Portier

## About

Tunfish manager and coordinator. Assigns clients to nodes, announces services.

## Quick setup

```sh
export TF_CA_URL=http://localhost:3333/
export TF_BROKER_URL=wss://localhost:8080/ws

make init
make run
```


## Verbose setup

### Create RSA key and get X.509 certificate
```sh
pip install pki-client

export TF_CA_URL=http://localhost:3333/
pki-client --ca-url=${TF_CA_URL} --ca-name=RootCA \
           --cacert=cacert.pem --key=portier.key --certificate=portier.pem --profile=client --common-name-prefix=portier
```

### Setup dependencies
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --editable .
```

### Invoke daemon
```sh
export TF_BROKER_URL=wss://localhost:8080/ws
TF_X509_CERT=portier.pem TF_X509_KEY=portier.key TF_X509_CACERT=cacert.pem AUTOBAHN_DEMO_ROUTER=${TF_BROKER_URL} tf-portier
```


## Tests
```sh
# Invoke PostgreSQL
docker run -it --rm --publish=5432:5432 --env=POSTGRES_HOST_AUTH_METHOD=trust postgres:13.2

# Invoke tests
make test

# Invoke tests with code coverage
make coverage
```
