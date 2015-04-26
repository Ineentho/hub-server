# Opidio Hub Server
[![Build Status](https://img.shields.io/circleci/project/opidio/hub-server.svg?style=flat-square)](https://circleci.com/gh/opidio/hub-server)
[![Code Coverage](https://img.shields.io/coveralls/opidio/hub-server.svg?style=flat-square)](https://coveralls.io/r/opidio/hub-server)

The Opidio Projects:

[![Hub Server](https://img.shields.io/badge/opidio-hub--server-blue.svg?style=flat-square)](https://github.com/opidio/hub-server)
[![Channel Server](https://img.shields.io/badge/opidio-channel--server-lightgray.svg?style=flat-square)](https://github.com/opidio/channel-server)
[![Android Client](https://img.shields.io/badge/opidio-android--client-lightgray.svg?style=flat-square)](https://github.com/opidio/android-client)
[![Landing Page](https://img.shields.io/badge/opidio-landing--page-lightgray.svg?style=flat-square)](https://github.com/opidio/landing-page)

The hub server aggregates multiple channel servers and provides an API for clients
(such as the Android client) to list all channels from one place. The hub server
is also the one responsible for handling user data.

## A note on docker

Using docker is completely optional, using a virtualenv should
work just as good, though docker is very convenient. If you
decide not to use Docker, you can use the `Dockerfile` and
`docker-compose.yml` as detailed step-by-step guides on how
to start the server or tests.

## Commands

### Starting the server

    docker-compose up

### Running the tests

    docker-compose run main ./runtests
