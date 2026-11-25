#!/usr/bin/env bash
# Quick health check: is the bot running, and what has it logged recently?
cd /opt/crypto-quant-platform && docker compose ps && echo && docker compose logs --tail 30 freqtrade
