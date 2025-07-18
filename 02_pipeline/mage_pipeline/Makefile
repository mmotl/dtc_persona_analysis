# the intention of this Makefile is 
# to provide a simple way to switch between local and cloud configurations for the mage pipeline
# by renaming the docker-compose files

cloud:
	mv docker-compose.yml docker-compose_local.yml
	mv docker-compose_cloud.yml docker-compose.yml

local:
	mv docker-compose.yml docker-compose_cloud.yml
	mv docker-compose_local.yml docker-compose.yml