SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
# Makefile Reference: https://tech.davis-hansson.com/p/make/

.PHONY: help sql migrate migrations debian ubuntu clean

# use HIDE to run commands invisibly, unless VERBOSE defined
HIDE:=$(if $(VERBOSE),,@)

export m		# Message for alembic migration
export revid	# Revision id to generate raw sql for
export rev1		# Previous revision id for generating migrations
export rev2		# New revision id for the new migration file

##
##|------------------------------------------------------------------------|
##			Help
##|------------------------------------------------------------------------|
help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/:\(.*\)##/:			/' | sed -e 's/##//'


##
##|------------------------------------------------------------------------|
##			Development
##|------------------------------------------------------------------------|
build: seed

seed:  # Seed the katalogus database
	-docker-compose run katalogus python -m boefjes.seed

##
##|------------------------------------------------------------------------|
##			Migrations
##|------------------------------------------------------------------------|

migrations: ## Generate a migration using alembic
ifeq ($(m),)
	$(HIDE) (echo "Specify a message with m={message} and a rev-id with revid={revid} (e.g. 0001 etc.)"; exit 1)
else
	docker-compose run katalogus python -m alembic --config /app/boefjes/boefjes/alembic.ini revision --autogenerate -m "$(m)"
endif


sql: ## Generate raw sql for the migrations
	docker-compose run katalogus python -m alembic --config /app/boefjes/boefjes/alembic.ini upgrade $(rev1):$(rev2) --sql

check:
	pre-commit run --all-files --color always

##
##|------------------------------------------------------------------------|
##			Tests
##|------------------------------------------------------------------------|

ci-docker-compose := docker-compose -f base.yml  -f .ci/docker-compose.yml


test: itest ## Run all tests.

itest: ## Run the integration tests.
	$(ci-docker-compose) build
	$(ci-docker-compose) down --remove-orphans
	$(ci-docker-compose) run --rm katalogus_integration

debian:
	docker run --rm \
	--env PKG_NAME=kat-boefjes \
	--env BUILD_DIR=./build \
	--env REPOSITORY=minvws/nl-kat-boefjes \
	--env RELEASE_VERSION=${RELEASE_VERSION} \
	--env RELEASE_TAG=${RELEASE_TAG} \
	--mount type=bind,src=${CURDIR},dst=/app \
	--mount type=bind,src=${CURDIR}/../octopoes,dst=/octopoes \
	--workdir /app \
	kat-debian-build-image \
	packaging/scripts/build-debian-package.sh

ubuntu:
	mkdir -p build
	docker run --rm \
	--env PKG_NAME=kat-boefjes \
	--env BUILD_DIR=./build \
	--env REPOSITORY=minvws/nl-kat-boefjes \
	--env RELEASE_VERSION=${RELEASE_VERSION} \
	--env RELEASE_TAG=${RELEASE_TAG} \
	--mount type=bind,src=${CURDIR},dst=/app \
	--mount type=bind,src=${CURDIR}/../octopoes,dst=/octopoes \
	--workdir /app \
	kat-ubuntu-build-image \
	packaging/scripts/build-debian-package.sh

clean:
	rm -rf build
	rm -rf debian/kat-*/ debian/.debhelper debian/files *.egg-info/ dist/
	rm debian/debhelper-build-stamp
	rm debian/*.*.debhelper
	rm debian/*.substvars
	rm debian/*.debhelper.log
	rm debian/changelog
