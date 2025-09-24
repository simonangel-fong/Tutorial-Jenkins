# Jenkins - Jenkins Configuration as Code

[Back](../README.md)

- [Jenkins - Jenkins Configuration as Code](#jenkins---jenkins-configuration-as-code)
  - [Prerequisites](#prerequisites)
  - [Plugins](#plugins)
  - [Configuration](#configuration)
  - [User](#user)
  - [Credential](#credential)
  - [jobs](#jobs)

---

## Prerequisites

- Installed `Configuration as Code` plugin

---

## Plugins

- Collect Installed Plugins:
  - Jenkins Console:

```groovy
// export plugins
Jenkins.instance.pluginManager.plugins.each {
  println("${it.getShortName()}: ${it.getVersion()}")
}
```

- Create a txt file:

  - plugins.txt

- copy in the dockefile

```dockerfile
# Install Jenkins plugins
COPY --chown=jenkins:jenkins ./config/plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
```

---

## Configuration

- jenkins.yaml

```yaml
jenkins:
  systemMessage: "Example of configuring credentials in Jenkins"
```

- Copy in the dockerfile

```dockerfile
# disable setup wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Setup Configuration as Code (CasC)
ENV CASC_JENKINS_CONFIG="/var/jenkins_home/casc_configs/jenkins.yaml"
COPY --chown=jenkins:jenkins ./config/jenkins.yaml /var/jenkins_home/casc_configs/jenkins.yaml
```

---

## User

```yaml
jenkins:
  securityRealm:
    local:
      allowsSignup: false
      enableCaptcha: false
      users:
        - id: ${JENKINS_ADMIN_ID}
          name: ${JENKINS_ADMIN_ID}
          password: ${JENKINS_ADMIN_PASSWORD}
```

---

## Credential

```yaml
jenkins:

credentials:
  system:
    domainCredentials:
      - credentials:
          - basicSSHUserPrivateKey: # credential type: ssh
              id: "vm-ssh-key"
              privateKeySource:
                directEntry:
                  privateKey: |
                    -----BEGIN OPENSSH PRIVATE KEY-----
                    your private key
                    -----END OPENSSH PRIVATE KEY-----
              scope: GLOBAL
              username: "jenkins"
              usernameSecret: true
```

---

## jobs

```yaml
jenkins:

jobs:
  - script: >
      pipelineJob('my_repo_pipeline') {
        definition {
          cpsScm {
            scm {
              git {
                remote {
                  url('https://github.com/simonangel-fong/Tutorial-Jenkins.git')
                }
                branch('*/master')
              }
            }
            scriptPath('module-docker-compose-JCasC/pipeline/Jenkinsfile')
          }
        }
      }
```

![pic](./pic/pipeline.png)
