# Variables
PYPROJECT = pyproject.toml
REGISTRY = crsimploncertif.azurecr.io
RG=RG-SIMPLON-CERTIF
IMAGE = ingestion-service
VERSION = $(shell grep -oP 'version = "\K[^"]+' $(PYPROJECT))
TAG = $(REGISTRY)/$(IMAGE):$(VERSION)

# Commandes
.PHONY: help build tag push login deploy test clean

help:
	@echo "Commandes disponibles :"
	@echo "  build   : Build l'image Docker"
	@echo "  tag     : Tag l'image pour le registry Azure"
	@echo "  push    : Push l'image vers Azure Container Registry"
	@echo "  login   : Login à Azure Container Registry"
	@echo "  deploy  : Build, tag, login et push (workflow complet)"
	@echo "  test    : Lance les tests Python"
	@echo "  clean   : Supprime les images locales"

build:
	pdm export -o requirements.txt --without-hashes
	docker build -t $(IMAGE):$(VERSION) -t $(IMAGE):latest .

tag:
	docker tag $(IMAGE):$(VERSION) $(TAG)

login:
	az acr login --name crsimploncertif

push:
	docker push $(TAG)

create-container:
	az containerapp create \
		--name $(IMAGE) \
		--resource-group $(RG) \
		--image $(REGISTRY)/$(IMAGE):$(VERSION) \
		--environment cae-simplon-certif \
		--target-port 8000 \
		--ingress external \
		--registry-server $(REGISTRY) \
		--user-assigned "id-simplon-certif-acr-deployer" \
		--registry-identity /subscriptions/de72360b-17c7-4771-9421-9ea5ed701ca2/resourcegroups/$(RG)/providers/Microsoft.ManagedIdentity/userAssignedIdentities/id-simplon-certif-acr-deployer \
		--query properties.configuration.ingress.fqdn

deploy-app:
	az containerapp update \
		--name $(IMAGE) \
		--resource-group $(RG) \
		--image $(REGISTRY)/$(IMAGE):$(VERSION)

create: build tag login push create-container

deploy: build tag login push deploy-app

test:
	pytest

clean:
	docker rmi $(IMAGE):$(VERSION) || true
	docker rmi $(TAG) || true
