#! /usr/bin/bash

cd /data/op/src/op-geth

/soft/op-node/geth \
  --datadir=/soft/op-node/data/  \
  --http \
  --http.port=8545\
  --http.addr=0.0.0.0 \
  --authrpc.addr=localhost \
  --authrpc.jwtsecret=/soft/op-node/jwt.txt \
  --verbosity=3 \
  --rollup.sequencerhttp=$SEQUENCER_URL \
  --nodiscover \
  --syncmode=full \
  --maxpeers=10 \
  --port=30303  \
  --authrpc.port=8551\
  --gcmode=full \
  --history.state=0     \
  --history.transactions=0


./op-node \
    --l1=https://ethereum.blockpi.network/v1/rpc/e1cf34328f54212022c29bea0fc2d3f2ac8ea88b  \
    --l1.rpckind=any \
    --l2=http://localhost:8551\
    --l2.jwt-secret=/soft/op-node/jwt.txt \
    --network=$NET \
    --rpc.addr=127.0.0.1 \
    --l1.trustrpc      \
    --rpc.port=8547

