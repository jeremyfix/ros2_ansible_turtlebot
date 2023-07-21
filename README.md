# What is this repository about ?

This repository contains ansible scripts to deploy a ROS2 installation on either turtlebot2 or turtlebot3

Before running the ansible playbook, we need to setup a basic installation and the procedure I found is not the same on the turtlebot3 (faster and easier) than for turtlebot2;

Working setup: 

- ubuntu 22.04
- ROS2 humble



# Basic installation

## Ansible ssh key generation

We first need to generate a ssh key that will be used for the ansible user 

```
mkdir ansible/keys
ssh-keygen -t rsa -b 2048 -f ansible/keys/id_rsa_ansible
```

Just press return to use an empty passphrase.

## Turtlebot2

For turtlebot2, our robots possess a laptop and the initial configuration is to install a ubuntu 22.04 server version on the laptop where we specifiy :

- user login : ubuntu
- user password : whatever you want

Then you need to create an ansible user. TO BE CONTINUED ...

## Turtlebot3 with RPI3

Our turtlebot3 are equiped with a raspberry pi 3. The steps to get the initial configuration is :

1- Burn with rpi imager a ubuntu 22.04 64 bits; Be sure to select the version for your raspberry 
2- modify and copy the files user-data meta-data and network-config to the system-boot partition

Taking the template files we provide, you need to bring in the following modifications

- in user-data: in the ssh_authorized_keys key, you need to paste the content of the `ansible/keys/id_rsa_ansible.pub` file,
- in user-data: change the name of the hostname so that it matches the DNS name,
- in network-config, you need to replace ROBOT_WIFI_SSID and ROBOT_WIFI_PASSWORD by their correct values.

Once the modifications are done and the files copied to the sd-card system-boot partition, you can then plugin the power and boot the system. It will automatically configure itself (autoinstall) given the content of the user-data, meta-data and network-config.

After, say , 5 - 10 minutes, you should be able to ping your robot and the following command should work :

```
ssh -i ansible/keys/id_rsa ansible@MYROBOTHOSTNAME
```


# Deploying ROS2 with ansible
