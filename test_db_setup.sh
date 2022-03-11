#!/bin/bash

dropdb -U postgres casting_test
createdb -U postgres casting_test
psql -U postgres -d casting_test -f casting_test.sql

export TEST_DATABASE_URL="postgresql://postgres:abc@localhost:5432/casting_test"