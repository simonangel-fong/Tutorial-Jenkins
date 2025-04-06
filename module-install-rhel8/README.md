# Jenkins - Install: RHEL 8.10

[Back](../README.md)

- [Jenkins - Install: RHEL 8.10](#jenkins---install-rhel-810)
  - [Docker: On Windows](#docker-on-windows)

## Docker: On Windows

- ref: https://www.jenkins.io/doc/book/installing/docker/#on-windows

---

```sh
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum upgrade -y
# Add required dependencies for the jenkins package
sudo yum install -y fontconfig java-17-openjdk
sudo yum install -y jenkins

sudo update-alternatives --config java
sudo systemctl daemon-reload

sudo systemctl enable --now jenkins

sudo systemctl status jenkins

sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --reload
```

- Access http://ip:8080


```sh
cat /var/lib/jenkins/secrets/initialAdminPassword
```