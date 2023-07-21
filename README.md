# What is this repository about ?

This repository contains ansible scripts to deploy a ROS2 installation on either turtlebot2 or turtlebot3

Before running the ansible playbook, we need to setup a basic installation and the procedure I found is not the same on the turtlebot3 (faster and easier) than for turtlebot2;

Working setup: 

- ubuntu 22.04
- ROS2 humble

These roles will :

- do the update/upgrade from apt
- setup the locale
- setup ntp
- setup the wifi
- update the firmware of the turtlebot3
- prevent power off when lid is closed on turtlebot2
- install ROS2 humble 
- configure a swap space on the turltbot3
- compile the ROS2 turtlebot packages (see roles turtlebot2 and turtlebot3)
- setup a rangle filter on the turtlebot2 (in our setup, we added a LDS scanner and the bones of the robot architecture hit the laser, these hits are filtered)
- install a systemd service to ensure a robot.launch.py launch file is ran on computer start  

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

Then you need to create an ansible user. 

In detail :

- you have to burn a ubuntu 22.04 server ISO with Startup Disk Creator
- then boot on the live USB and once the GRUB pops out, edit the line "Try or install" and adds the "autoinstall" :

```
linux   /casper/vmlinuz autoinstall quiet 
```
Then run this entry.

Answer all the questions, basically on my side :

- Set English as the language ,  but French for the keyboard
- set up the WIFI to connect to our SSID  and wait for the connection to be established
- tick the box "Install OpenSSH" 
- username :  ubuntu   with password   turtlebot
- hostname, but the ansible roles will fix that anyway
- do not change anything for the disk layout, use the whole drive as suggested, do not changed anything on the snap package list they propose

Once install, reboot. Then SSH to the turtlebot and :

```
sudo adduser ansible
```

The password can be random, you just need to keep it in mind for the following command

From your terminal :

```
ssh-copy-id -i ansible/keys/id_rsa_ansible.pub ansible@YOUR_TURTLEBOT_HOSTNAME
```

There, that's the only place you need to provide the password. Then you can forget about it.

Finally, create a file    `sudo vim /etc/sudoers.d/ansible` with the following content :

```
ansible  ALL=(ALL) NOPASSWD:ALL
```

Then, from there, ansible user can sudo with password and you can proceed with [Deploying ROS2 with ansible](#deploying-ros2-with-ansible) section.

## Turtlebot3 with RPI3

Our turtlebot3 are equiped with a raspberry pi 3. The steps to get the initial configuration is :

1- Burn with rpi imager a ubuntu 22.04 64 bits; Be sure to select the version for your raspberry 
2- modify and copy the files user-data meta-data and network-config to the system-boot partition

Taking the template files we provide in `turtlebot3_basic/`, you need to bring in the following modifications

- in user-data: change the name of the hostname so that it matches the DNS name,
- in network-config, you need to replace ROBOT_WIFI_SSID and ROBOT_WIFI_PASSWORD by their correct values.

Once the modifications are done and the files copied to the sd-card system-boot partition, you can then plugin the power and boot the system. It will automatically configure itself (autoinstall) given the content of the user-data, meta-data and network-config.

After, say , 5 - 10 minutes, you should be able to ping your robot and the following command should work :

```
ssh -i ansible/keys/id_rsa ansible@MYROBOTHOSTNAME
```

and the login should be performed without asking for a password.

# Deploying ROS2 with ansible

## Setting up the inventory

The list of turtlebots you want to deploy is specified in the `ansible/etc/hosts` file. There are two dummy entries. You need to adapt this file with your settings.

One of the role is ensuring the wifi is correctly setup, you need to define two eenvironment variables and then run the playbook

```
export ROBOT_WIFI_SSID=xxxxx
export ROBOT_WIFI_PASSWORD=xxxx
cd ansible
./scripts/run-playbook.sh install.yml turtlebot_hosts
```

If you want to apply the playbook to only one host, you can change the playbook execution to only this host :

```
./scripts/run-playbook.sh install.yml dummy.hostname.for_turtle3
```

Then it will take some time. On turtlebot3, around 2hours. On turtlebot2, I do not remember how much time, certainly faster than turtlebot3.
