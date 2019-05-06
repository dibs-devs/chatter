#!/bin/bash

# Clear migrations
rm -rf django_chatter/migrations
rm -rf django_chatter/__pycache__/
rm -rf chatter/migrations
rm -rf chatter/__pycache__/

# Clear postgres chatter db and recreate
psql -U postgres -c 'drop database if exists chatter;'
psql -U postgres -c 'create database chatter;'
psql -U postgres -c "grant all privileges on database chatter to chatteradmin;"
psql -U postgres -c "alter role chatteradmin createdb;"
