#!/bin/bash
# Cycles turning redis on and off for testing purposes
# Usage: ./redis_cycle.sh

CONTAINER_NAME="my-redis"
SLEEP_DURATION=15 # Example: stop/start every 15 seconds

while true; do
  # Stop the container
  echo "Stopping $CONTAINER_NAME container..."
  docker stop $CONTAINER_NAME

  # Sleep for half the duration
  echo "Sleeping for $(($SLEEP_DURATION / 2)) seconds..."
  sleep $(($SLEEP_DURATION / 2))

  # Start the container
  echo "Starting $CONTAINER_NAME container..."
  docker start $CONTAINER_NAME

  # Sleep for the other half of the duration
  echo "Sleeping for $(($SLEEP_DURATION / 2)) seconds..."
  sleep $(($SLEEP_DURATION / 2))
done
