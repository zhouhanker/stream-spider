#!/bin/bash
#
# start and stop etherum
# author: 2024 han.zhou

# generate jwt
# openssl rand -hex 32 | tr -d "\n" > "jwt.hex"

local_host=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}')
http_port=8545
auth_rpc_port=8551
etherum_dir="/soft/etherum"
etherum_consensus_dir="$etherum_dir/consensus"
etherum_execution_dir="$etherum_dir/execution"
jwt_hex="$etherum_dir/jwt.hex"
prysm_data_path="$etherum_consensus_dir/prysm-data/"
geth_data_path="$etherum_execution_dir/data/"
geth_log_path="$etherum_dir/geth.log"
prysm_log_path="$etherum_dir/prysm.log"


start_etherum(){
  echo "Etherum Node start Run Geth And Prysm ..."
  nohup $etherum_execution_dir/geth \
  --datadir $geth_data_path \
  --syncmode snap --gcmode archive \
  --txlookuplimit 0 --cache 30000 \
  --maxpeers 9999 \
  --maxpendpeers 100 \
  --http --http.addr $local_host \
  --http.port $http_port \
  --http.api eth,net,engine,admin,web3 \
  --verbosity 3 \
  --authrpc.addr $local_host \
  --authrpc.port $auth_rpc_port \
  --authrpc.vhosts $local_host \
  --authrpc.jwtsecret $jwt_hex >$geth_log_path 2>&1 &

  nohup sh $etherum_consensus_dir/prysm.sh \
  beacon-chain --execution-endpoint=http://$local_host:$auth_rpc_port \
  --jwt-secret=$jwt_hex \
  --datadir $prysm_data_path \
  --accept-terms-of-use=true \
  --block-batch-limit 5 > $prysm_log_path 2>&1 &
  echo "Geth And Prysm Running ......"
}

stop_etherum(){
  echo "Etherum Node Stop Geth And Prysm ..."
  # Geth
  if ps aux | grep -q '[g]eth'; then
  # Get Geth PID
  geth_pid=$(pgrep -o '[g]eth')
  echo "Terminating geth process with PID $geth_pid..."
  kill -9 $geth_pid
  else
    echo "No running geth process found."
  fi

  if ps aux | grep -q '[p]rysm'; then
  # Get Prysm PID
  prysm_pid=$(pgrep -o '[p]rysm')
  echo "Terminating prysm process with PID $prysm_pid..."
  kill -9 $prysm_pid
  else
    echo "No running prysm process found."
  fi
}

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <action>"
  exit 1
fi

action=$1

# 根据参数值执行不同的方法
case "$action" in
  start)
    start_etherum
    ;;
  stop)
    stop_etherum
    ;;
  *)
    echo "Invalid action: $action. Please use 'start' or 'stop'."
    exit 1
    ;;
esac