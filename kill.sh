#!/bin/sh

lsof -t -i tcp:8000 | xargs kill -9
