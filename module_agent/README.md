# Jenkins - Agent

[Back](../README.md)

- [Jenkins - Agent](#jenkins---agent)
  - [VM agent](#vm-agent)
    - [Set up Agent Node (Ubuntu)](#set-up-agent-node-ubuntu)
    - [Configure SSH Credential](#configure-ssh-credential)

---

## VM agent

### Set up Agent Node (Ubuntu)

```sh
sudo apt update
sudo apt install -y openjdk-17-jre openssh-server
java --version

# Create jenkins user
sudo useradd jenkins -d /home/jenkins -m -s /bin/bash
sudo mkdir -pv /home/jenkins/agent && sudo chown -Rv jenkins:jenkins /home/jenkins
# set pwd
sudo passwd jenkins
```

- Create keys and copy to Agent node

```sh
# linux copy key to linux
ssh-keygen  # default id_ed25519
ssh-copy-id jenkins@on-prem

# Windows compy key to linux: powershell
# cd to user dir
type ".ssh\id_ed25519.pub" | ssh jenkins@on-prem "mkdir -pv .ssh; cat >> .ssh/authorized_keys"

ssh jenkins@on-prem
```

---

### Configure SSH Credential

install SSH Agent

- `jenkins_ssh`

/home/jenkins/agent