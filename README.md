# Opidio hub server
[![Build Status](https://img.shields.io/circleci/project/opidio/hub-server.svg?style=flat-square)](https://circleci.com/gh/opidio/hub-server)
[![Code Coverage](https://img.shields.io/coveralls/opidio/hub-server.svg?style=flat-square)](https://coveralls.io/r/opidio/hub-server)

[![Hub Server](https://img.shields.io/badge/opidio-hub--server-blue.svg?style=flat-square)](/opidio/hub-server)
[![Channel Server](https://img.shields.io/badge/opidio-channel--server-lightgray.svg?style=flat-square)](/opidio/channel-server)
[![Android Client](https://img.shields.io/badge/opidio-android--client-lightgray.svg?style=flat-square)](/opidio/android-client)

The user facing hub-server that aggregates multiple channel-servers

## A note on docker

Using docker is completely optional, using a virtualenv should
work just as good, though docker is very convenient. If you
decide not to use Docker, you can use the `Dockerfile` and
`docker-compose.yml` as detailed step-by-step guides on how
to start the server or tests.

## Commands

### Starting the server

    sudo docker-compose up

### Running the tests

    sudo docker-compose run main ./runtests