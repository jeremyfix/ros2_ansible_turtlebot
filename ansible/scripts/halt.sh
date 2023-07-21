#!/bin/sh

if [ "$#" -ne 1 ]
then
	echo "Usage: ${0} <host_limit1[,host_limit2[,...]]>"
	exit 1
fi

host_limit="${1}"

(
	cd $(dirname "${0}")/.. && \
	ANSIBLE_INVENTORY=etc/hosts \
	ANSIBLE_ROLES_PATH=roles \
	ansible ${host_limit} --user=ansible --private-key=./keys/id_rsa_ansible \
	-e ansible_python_interpreter=/usr/bin/python3 \
	-m shutdown
)
