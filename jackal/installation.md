##### Jackal Node Installation Guide

https://app.nodejumper.io/jackal/installation

https://polkachu.com/tendermint_snapshots/jackal


##### Vote
```
canined tx gov vote 26 yes --from wallet --chain-id jackal-1 --gas-adjustment 1.4 --gas auto --gas-prices 0.025ujkl -y
```

##### Show Wallet key
```
canined keys show wallet -a
```

##### Get wallet balance
```
canined q bank balances $(canined keys show wallet -a) --node https://jackal-rpc.noders.services:443
```

##### Withdraw rewards and commission
```
canined tx distribution withdraw-rewards $(canined keys show wallet --bech val -a) --commission --from wallet --chain-id jackal-1 --gas-adjustment 1.5 --gas auto --gas-prices 0.025ujkl -y
```