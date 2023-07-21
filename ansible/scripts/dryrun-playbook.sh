#!/bin/sh

# To limit a run to a specific set of hosts, use e.g. :
# ansible-playbook --list-hosts -l hosts_AT_rennes [...] openldap-slave.yml
# Option --list-hosts will only list hosts ; remove it to execute playbook
# Use options -C and -D to check (only) diffs of templates and files

# To start at a specific task and perform operations step by step, use e.g. :
# ansible-playbook --start-at-task 'Set hostname' --step

if [ -z "${1}" ] || [ ! -f "${1}" ]
then
	echo "Usage: ${0} <playbook.yml> [host_limit1[,host_limit2[,...]]]"
	exit 1
fi

host_limit=""
[ -n "${2}" ] && \
	host_limit="-l ${2}"

yml_file=$(readlink -f "${1}")

(
	cd $(dirname "${0}")/.. && \
	ANSIBLE_INVENTORY=etc/hosts \
	ANSIBLE_CONFIG=etc/ansible.cfg \
	ansible-playbook --user=ansible --private-key=./keys/id_rsa_ansible \
	--check --diff \
	-e ansible_python_interpreter=/usr/bin/python3 \
	-b ${host_limit} "${yml_file}"
)
