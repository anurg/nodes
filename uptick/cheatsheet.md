### Uptick commands
- Recover wallet
```
uptickd keys add wallet --recover
```
- Vote
```
uptickd tx gov vote 1 yes --from wallet --chain-id uptick_117-1  --gas 250000 --fees 3000000000000000auptick -y

```

- Unbond tokens
```
uptickd tx staking unbond $(uptickd keys show wallet --bech val -a) 3000000000000000000auptick --from wallet --chain-id uptick_117-1  --gas 250000 --fees 3000000000000000auptick -y
```

- Bank balances
```
uptickd q bank balances $(uptickd keys show wallet -a)
```
##### Keys Export ETH
```
uptickd keys  unsafe-export-eth-key wallet
```

###### Withdraw rewards and commission from your validator
```
uptickd tx distribution withdraw-rewards $(uptickd keys show $WALLET --bech val -a) --from wallet --commission --chain-id uptick_117-1 --gas 250000 --fees 3000000000000000auptick -y 
```
#### Validator Address
```
echo $(uptickd keys show $WALLET --bech val -a)
```

##### Bank Balances
```
uptickd q bank balances wallet
```