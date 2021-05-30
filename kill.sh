#!/bin/sh

port=8000

lsof -t -i tcp:$port | xargs kill -9
