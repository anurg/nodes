#### Dependencies Installation

##### Install dependencies for building from source
```
sudo apt update
sudo apt install -y curl git jq lz4 build-essential
```

# Install Go
```
sudo rm -rf /usr/local/go
curl -L https://go.dev/dl/go1.22.7.linux-amd64.tar.gz | sudo tar -xzf - -C /usr/local
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> $HOME/.profile
source .profile
```

#### Node Installation
##### Clone project repository
```
cd && rm -rf uptick
git clone https://github.com/UptickNetwork/uptick
cd uptick
git checkout v0.3.0
```

##### Build binary
```
make install
```

##### Prepare cosmovisor directories
```
mkdir -p $HOME/.uptickd/cosmovisor/genesis/bin
ln -s $HOME/.uptickd/cosmovisor/genesis $HOME/.uptickd/cosmovisor/current -f
```

##### Copy binary to cosmovisor directory
```
cp $(which uptickd) $HOME/.uptickd/cosmovisor/genesis/bin
```

##### Set node CLI configuration
```
uptickd config set client chain-id uptick_117-1
uptickd config set client keyring-backend file
uptickd config set client node tcp://localhost:20457
```
##### Initialize the node
```
uptickd init "nkbblocks" --chain-id uptick_117-1
```

##### Download genesis and addrbook files
```
curl -L https://snapshots.nodejumper.io/uptick/genesis.json > $HOME/.uptickd/config/genesis.json
curl -L https://snapshots.nodejumper.io/uptick/addrbook.json > $HOME/.uptickd/config/addrbook.json
```

##### Set seeds
```
sed -i -e 's|^seeds *=.*|seeds = "e71bae28852a0b603f7360ec17fe91e7f065f324@uptick-mainnet-seed.itrocket.net:35656,df949a46ae6529ae1e09b034b49716468d5cc7e9@seeds.stakerhouse.com:10656,bddaa78825892bde04b5aa8f28b95a072a50eaf9@mainnet.seednode.citizenweb3.com:29656,dd482d080820020b144ca2efaf128d78261dea82@uptick-mainnet-peer.itrocket.net:10656,c65c6ecfb60635fc8a076b6f90fcd2607aceaa64@uptick.peers.stavr.tech:3156,37604dc6535a2f1b91e38c35f77b5be4a93c35b2@45.77.168.172:26656,bddaa78825892bde04b5aa8f28b95a072a50eaf9@78.46.79.242:29656"|' $HOME/.uptickd/config/config.toml
```

#### Set minimum gas price
```
sed -i -e 's|^minimum-gas-prices *=.*|minimum-gas-prices = "13000000000auptick"|' $HOME/.uptickd/config/app.toml
```

##### Set pruning
```
sed -i \
  -e 's|^pruning *=.*|pruning = "custom"|' \
  -e 's|^pruning-keep-recent *=.*|pruning-keep-recent = "100"|' \
  -e 's|^pruning-interval *=.*|pruning-interval = "17"|' \
  $HOME/.uptickd/config/app.toml
```

##### Enable prometheus
```
sed -i -e 's|^prometheus *=.*|prometheus = true|' $HOME/.uptickd/config/config.toml
```

##### Change ports
```
sed -i -e "s%:1317%:20417%; s%:8080%:20480%; s%:9090%:20490%; s%:9091%:20491%; s%:8545%:20445%; s%:8546%:20446%; s%:6065%:20465%" $HOME/.uptickd/config/app.toml
sed -i -e "s%:26658%:20458%; s%:26657%:20457%; s%:6060%:20460%; s%:26656%:20456%; s%:26660%:20461%" $HOME/.uptickd/config/config.toml
```

##### Download latest chain data snapshot
```
curl "https://snapshots.nodejumper.io/uptick/uptick_latest.tar.lz4" | lz4 -dc - | tar -xf - -C "$HOME/.uptickd"
```

##### Install Cosmovisor
```
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@v1.7.0
```

#### Create a service
```
sudo tee /etc/systemd/system/uptick.service > /dev/null << EOF
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
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable uptick.service
```

#### Start the service and check the logs
```
sudo systemctl start uptick.service
sudo journalctl -u uptick.service -f --no-hostname -o cat
```
-----

### Secure Server Setup (Optional)

##### generate ssh keys, if you don't have them already, DO IT ON YOUR LOCAL MACHINE
```
ssh-keygen -t rsa
```

# save the output, we'll use it later on instead of YOUR_PUBLIC_SSH_KEY
```
cat ~/.ssh/id_rsa.pub
```
##### upgrade system packages
```
sudo apt update
sudo apt upgrade -y
```

##### add new admin user
```
sudo adduser admin --disabled-password -q
```

#### upload public ssh key, replace YOUR_PUBLIC_SSH_KEY with the key above
```
mkdir /home/admin/.ssh
echo "YOUR_PUBLIC_SSH_KEY" >> /home/admin/.ssh/authorized_keys
sudo chown admin: /home/admin/.ssh
sudo chown admin: /home/admin/.ssh/authorized_keys

echo "admin ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
```
##### disable root login, disable password authentication, use ssh keys only
```
sudo sed -i 's|^PermitRootLogin .*|PermitRootLogin no|' /etc/ssh/sshd_config
sudo sed -i 's|^ChallengeResponseAuthentication .*|ChallengeResponseAuthentication no|' /etc/ssh/sshd_config
sudo sed -i 's|^#PasswordAuthentication .*|PasswordAuthentication no|' /etc/ssh/sshd_config
sudo sed -i 's|^#PermitEmptyPasswords .*|PermitEmptyPasswords no|' /etc/ssh/sshd_config
sudo sed -i 's|^#PubkeyAuthentication .*|PubkeyAuthentication yes|' /etc/ssh/sshd_config

sudo systemctl restart sshd
```
# install fail2ban
```
sudo apt install -y fail2ban
```
# install and configure firewall
```
sudo apt install -y ufw
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow 9100
sudo ufw allow 26656
```
# make sure you expose ALL necessary ports, only after that enable firewall
```
sudo ufw enable
```
# make terminal colorful
```
sudo su - admin
source <(curl -s https://raw.githubusercontent.com/nodejumper-org/cosmos-scripts/master/utils/enable_colorful_bash.sh)
```

# update servername, if needed, replace YOUR_SERVERNAME with wanted server name
```
sudo hostnamectl set-hostname YOUR_SERVERNAME
```
# now you can logout (exit) and login again using ssh admin@YOUR_SERVER_IP

https://itrocket.net/services/mainnet/uptick/installation/

```
# Install Go
sudo rm -rf /usr/local/go
curl -L https://go.dev/dl/go1.22.7.linux-amd64.tar.gz | sudo tar -xzf - -C /usr/local
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> $HOME/.profile
source .profile
```

```
# Set node CLI configuration
uptickd config set client chain-id uptick_117-1
uptickd config set client keyring-backend file
uptickd config set client node tcp://localhost:20457
```