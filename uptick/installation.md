https://itrocket.net/services/mainnet/uptick/installation/

##### Uptick Node Installation

```
# install dependencies, if needed
sudo apt update && sudo apt upgrade -y
sudo apt install curl git wget htop tmux build-essential jq make lz4 gcc unzip -y
```

##### Install Go

```
sudo rm -rf /usr/local/go
curl -L https://go.dev/dl/go1.23.8.linux-amd64.tar.gz | sudo tar -xzf - -C /usr/local
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> $HOME/.bash_profile
source $HOME/.bash_profile
```

##### Set Environment Variables

```
# set vars
echo "export WALLET="wallet"" >> $HOME/.bash_profile
echo "export MONIKER="nkbblocks"" >> $HOME/.bash_profile
echo "export UPTICK_CHAIN_ID="uptick_117-1"" >> $HOME/.bash_profile
echo "export UPTICK_PORT="35"" >> $HOME/.bash_profile
source $HOME/.bash_profile
```

##### # download binary

```
cd $HOME
rm -rf uptick
git clone https://github.com/UptickNetwork/uptick.git
cd uptick
git checkout v0.3.0
```

##### Build binaries

```
make build
```

##### Prepare binaries for Cosmovisor

```
mkdir -p $HOME/.uptickd/cosmovisor/genesis/bin
mv build/uptickd $HOME/.uptickd/cosmovisor/genesis/bin/
rm -rf build
```

##### Create application symlinks

```
ln -s $HOME/.uptickd/cosmovisor/genesis $HOME/.uptickd/cosmovisor/current -f
sudo ln -s $HOME/.uptickd/cosmovisor/current/bin/uptickd /usr/local/bin/uptickd -f
```

##### # config and init app

```
uptickd config set client node tcp://localhost:${UPTICK_PORT}657
uptickd config set client keyring-backend os
uptickd config set client chain-id uptick_117-1
uptickd init "nkbblocks" --chain-id uptick_117-1
```

###### download genesis and addrbook

```
wget -O $HOME/.uptickd/config/genesis.json https://server-3.itrocket.net/mainnet/uptick/genesis.json
wget -O $HOME/.uptickd/config/addrbook.json  https://server-3.itrocket.net/mainnet/uptick/addrbook.json
```

###### set seeds and peers

```
SEEDS="e71bae28852a0b603f7360ec17fe91e7f065f324@uptick-mainnet-seed.itrocket.net:35656"
PEERS="dd482d080820020b144ca2efaf128d78261dea82@uptick-mainnet-peer.itrocket.net:10656,1ec3f0994e9846d9cde42a6c3e4232228ccb0e7e@65.109.53.24:35656,3d797f708f1f210e2e7ac5875d7a18586c0f6f8d@46.37.123.53:26656,ee045c74c0678f1122650a3a5223923977cae1b3@65.109.93.152:30656,ccb5574802476107befcfdb79867a942008fdd82@167.235.9.223:61156,c21eeb897d3fa45a81772b56038045d1d873252e@142.132.199.236:30656,d437de9c0b06e4270206a789fcefbb75973a5bb8@167.235.2.246:43756,ea9c7688fa12f96c13cb37692fb129a780f6660e@65.109.88.251:11096,6af07daddb8a57c01d05d8c0894f8293a41090d0@144.76.195.75:45056,446de8c68b97e25bb48e8460eae8f0eb49aa5d62@46.4.55.46:21656,90c0c03d27e5b4354bffb709d28340f2657ca1c7@138.201.121.185:26679,8ecd3260a19d2b112f6a84e0c091640744ec40c5@185.165.241.20:26666,14ca9d73314dd519bc0b0be8511c88f85fe6873e@46.4.81.204:17656,c7abddafe697b2a75a1567e0fe274d919e5fa404@65.109.106.214:15656,bd2e1f218fde74045fbcff3fe36c467e7f05d7a3@198.244.165.50:21656,0cba8f6d9de4a017c382f57e5389f0ad138605f4@144.76.74.73:15956,446a4b3a6dcfc8f6c55dc02ce49e98936a713920@176.9.92.135:60756,37e4491bd756cf0ae5281c6f0da4bdcefe723eba@135.181.109.175:15656,f7d2088f31ea5b0a172b66b3c5edabdfd18cd4e9@[2a01:4f9:c011:89db::1]:26656"
sed -i -e "/^\[p2p\]/,/^\[/{s/^[[:space:]]*seeds *=.*/seeds = \"$SEEDS\"/}" \
       -e "/^\[p2p\]/,/^\[/{s/^[[:space:]]*persistent_peers *=.*/persistent_peers = \"$PEERS\"/}" $HOME/.uptickd/config/config.toml
```

##### # set custom ports in app.toml

```
sed -i.bak -e "s%:1317%:${UPTICK_PORT}317%g;
s%:8080%:${UPTICK_PORT}080%g;
s%:9090%:${UPTICK_PORT}090%g;
s%:9091%:${UPTICK_PORT}091%g;
s%:8545%:${UPTICK_PORT}545%g;
s%:8546%:${UPTICK_PORT}546%g;
s%:6065%:${UPTICK_PORT}065%g" $HOME/.uptickd/config/app.toml
```

##### # set custom ports in config.toml file

```
sed -i.bak -e "s%:26658%:${UPTICK_PORT}658%g;
s%:26657%:${UPTICK_PORT}657%g;
s%:6060%:${UPTICK_PORT}060%g;
s%:26656%:${UPTICK_PORT}656%g;
s%^external_address = \"\"%external_address = \"$(wget -qO- eth0.me):${UPTICK_PORT}656\"%;
s%:26660%:${UPTICK_PORT}660%g" $HOME/.uptickd/config/config.toml
```

##### # config pruning

```
sed -i -e "s/^pruning *=.*/pruning = \"custom\"/" $HOME/.uptickd/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"100\"/" $HOME/.uptickd/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"19\"/" $HOME/.uptickd/config/app.toml
```

##### # set minimum gas price, enable prometheus and disable indexing

```
sed -i 's|minimum-gas-prices =.*|minimum-gas-prices = "0.0025auptick"|g' $HOME/.uptickd/config/app.toml
sed -i -e "s/prometheus = false/prometheus = true/" $HOME/.uptickd/config/config.toml
sed -i -e "s/^indexer *=.*/indexer = \"null\"/" $HOME/.uptickd/config/config.toml
```

##### Install Cosmovisor

```
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@v1.7.0
```

##### # create service file

```
# Create a service
sudo tee /etc/systemd/system/uptickd.service > /dev/null << EOF
[Unit]
Description=Uptick node service
After=network-online.target
[Service]
User=$USER
WorkingDirectory=$HOME/.uptickd
ExecStart=$(which cosmovisor) run start
Restart=on-failure
RestartSec=5
LimitNOFILE=65535
Environment="DAEMON_HOME=$HOME/.uptickd"
Environment="DAEMON_NAME=uptickd"
Environment="UNSAFE_SKIP_BACKUP=true"
Environment="DAEMON_ALLOW_DOWNLOAD_BINARIES=true"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$HOME/.uptickd/cosmovisor/current/bin"
[Install]
WantedBy=multi-user.target
EOF
```

##### # reset and download snapshot

```
uptickd tendermint unsafe-reset-all --home $HOME/.uptickd
if curl -s --head curl https://server-3.itrocket.net/mainnet/uptick/uptick_2026-04-02_16657171_snap.tar.lz4 | head -n 1 | grep "200" > /dev/null; then
  curl https://server-3.itrocket.net/mainnet/uptick/uptick_2026-04-02_16657171_snap.tar.lz4 | lz4 -dc - | tar -xf - -C $HOME/.uptickd
    else
  echo "no snapshot found"
fi
```

##### # enable and start service

```
sudo systemctl daemon-reload
sudo systemctl enable uptickd
sudo systemctl restart uptickd && sudo journalctl -u uptickd -fo cat
```
