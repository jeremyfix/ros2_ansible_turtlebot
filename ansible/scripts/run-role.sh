#!/bin/sh

# To limit a run to a specific set of hosts, use e.g. :
# ansible-playbook --list-hosts -l hosts_AT_rennes [...] openldap-slave.yml
# Option --list-hosts will only list hosts ; remove it to execute playbook
# Use options -C and -D to check (only) diffs of templates and files

# To start at a specific task and perform operations step by step, use e.g. :
# ansible-playbook --start-at-task 'Set hostname' --step

if [ "$#" -ne 2 ]
then
	echo "Usage: ${0} <role> <host_limit1[,host_limit2[,...]]>"
	exit 1
fi

host_limit="${2}"
roles="${1}"

(
	cd $(dirname "${0}")/.. && \
	ANSIBLE_INVENTORY=etc/hosts \
	ANSIBLE_CONFIG=etc/ansible.cfg \
	ANSIBLE_ROLES_PATH=roles \
	ansible-playbook --user=ansible --private-key=./keys/id_rsa_ansible \
	-e ansible_python_interpreter=/usr/bin/python3 \
	-b -l ${host_limit} /dev/stdin <<END
---
- hosts : $host_limit
  roles :
    - $roles
END
)
