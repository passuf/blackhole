#!/usr/bin/env bash
set -e  # abort if one command fails

# Connect to the host
ssh dalek "bash -s" < dalek_deploy_commands.sh
