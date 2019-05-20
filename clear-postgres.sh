#!/bin/bash

# Clear postgres chatter db and recreate
psql -U postgres -c 'drop database if exists chatter;'
psql -U postgres -c 'create database chatter;'
psql -U postgres -c "grant all privileges on database chatter to chatteradmin;"
psql -U postgres -c "alter role chatteradmin createdb;"
