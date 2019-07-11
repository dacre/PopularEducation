# PopularEducation

This project aims to collect Swedish (first out Stockholm) public seminars in a easy to access and easy to search manner so that people easier can educate themselves in interesting topics.

Currently Stockholm University and Folkuniversitet are supported from a scraping point of view. The results are put in a HTML table.

This project is (soon) live at http://bildningstid.se:5000 

## Some of the planned work:
- make the frontend
   - Ideas:
      - https://getbootstrap.com/docs/4.0/components/list-group/#custom-content 
      - https://foundation.zurb.com/building-blocks/blocks/dashboard-table.html
      - https://bootsnipp.com/snippets/peZX7
- add more sources (KTH for example)
- setup with Let's Encrypt (possibly using nginx as a proxy)
- setup with Ansible or similar to simplify VPS switch in the future
- add analytics using access log analysis, possibly via https://goaccess.io/

## Installation steps for a Debian based VPS


### Setup (Swedish) locale

```
export LANGUAGE=sv_SE.UTF-8
export LC_ALL=sv_SE.UTF-8
export LANG=sv_SE.UTF-8
export LC_TYPE=sv_se.UTF-8
sudo locale-gen
sudo dpkg-reconfigure locales
```


### Setup non-root user (reusing root's public RSA key)
```
adduser dacre
sudo adduser dacre sudo
id dacre

sudo mkdir /home/dacre/.ssh/
sudo cp .ssh/authorized_keys /home/dacre/.ssh/authorized_keys
sudo chmod 604 /home/dacre/.ssh/authorized_keys
```

### Setup more secure SSH
Tips from: https://linux-audit.com/audit-and-harden-your-ssh-configuration/

Backup the file first
```
cp /etc/ssh/sshd_config /root/sshd_config
```
Do the following changes in sshd_config:
```
X11Forwarding no
PermitEmptyPasswords no
MaxAuthTries 6
PubkeyAuthentication yes
PasswordAuthentication no
PermitRootLogin no
AllowUsers dacre
```
```
sudo systemctl restart ssh
```
### Additional protection against brute force attacks 

Tips from: https://www.vultr.com/docs/how-to-setup-fail2ban-on-debian-9-stretch

```
sudo apt update && apt upgrade -y
sudo apt install fail2ban -y

systemctl status fail2ban 
```


### Setup Docker (for Debian)

Tips from: https://docs.docker.com/install/linux/docker-ce/debian/
```
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
   
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo docker run hello-world   
sudo usermod -aG docker dacre
sudo systemctl enable docker
sudo systemctl start docker
```
### Setup docker-compose (for Debian)
Tips from: https://docs.docker.com/compose/install/

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
docker-compose --version
	OUTPUT: docker-compose version 1.24.0, build 0aa59064
```

### Download PopularEducation
```
sudo apt-get install git

git clone https://github.com/dacre/PopularEducation.git
cd PopularEducation/

(Remember to modify docker-compose.yml to the correct path for you, for example: /home/dacre/PopularEducation/importer/db)
```
### Actually running PopularEducation!
```
docker-compose build && docker-compose up 
```