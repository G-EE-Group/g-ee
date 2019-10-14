# Docker
This directory contains deployable docker containers for scripts. These will eventually be built automatically in a public repo on https://hub.docker.com

# Contributing

Your Docker container must be in its own sub directory in this directory!

e.g. `Docker/NEW CONTAINER/Dockerfile`

- Please include all neccessary files for your Docker container in the same folder as your DockerFile.
- Docker containers must support either a .env file or environment variables for deploying with configs.
  - Docker Swarm support would be appreciated! (Secrets, etc) :)
- Include a README.md file for your container to explain how its used.
- Please mark whether your container is "Cross Platform, Windows Only, Linux Only"!
