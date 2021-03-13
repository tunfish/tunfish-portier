include util.mk


# =============
# Configuration
# =============

$(eval tf-portier   := $(venv)/bin/tf-portier)
$(eval pki-client   := $(venv)/bin/pki-client)


# =====
# Setup
# =====

# Install requirements for development.
setup-package: setup-virtualenv
	@test -e $(tf-portier) || $(pip) install --editable .


# ====
# Init
# ====
init: setup-package
	$(pip) install pki-client
	$(pki-client) \
        --ca-url=$(TF_CA_URL) --ca-name=RootCA \
        --cacert=cacert.pem --key=portier.key --certificate=portier.pem --profile=client --common-name-prefix=broker


# ===
# Run
# ===
run:
	TF_X509_CERT=portier.pem TF_X509_KEY=portier.key TF_X509_CACERT=cacert.pem AUTOBAHN_DEMO_ROUTER=${TF_BROKER_URL} $(tf-portier)
