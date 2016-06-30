#!/usr/bin/python

from ansible.module_utils.basic import *
import virtualbox

def virtualbox_guest_present(data):

	vbox = virtualbox.VirtualBox()
	guest = vbox.create_machine(
	        settings_file = "",
	        name = data["name"],
	        groups = [],
	        os_type_id = data["os_type"],
	        flags = "" 
	        )
	
	guest.cpu_count = data["vcpu"]
	guest.memory_size = data["memory"]

	vbox.register_machine(guest)

	has_changed = True
	meta = { "present": "success" }
	return (has_changed, meta)

def virtualbox_guest_absent(data):

	vbox = virtualbox.VirtualBox()
	guest = vm = vbox.find_machine(data["name"])
	guest.unregister(cleanup_mode=virtualbox.library.CleanupMode.full)

	has_changed = True
	meta = { "present": "success" }
	return (has_changed, meta)

def main():

	fields = {
		"name": { "required": True, "type": "str" },
		"vcpu": { "default": 1, "type": "int" },
		"memory": { "default": 2048, "type": "int" },
		"os_type":{
			"required": True, 
			"choices": [ "Windows2012_64", "Windows2008_64" ],
			"type": "str" },
		"state": {
			"default": "present",
			"choices": [ "present", "absent" ],
			"type": "str"
		}
	}

	choice_map = {
		"present": virtualbox_guest_present,
		"absent": virtualbox_guest_absent
	}

	module = AnsibleModule(argument_spec=fields)
	has_changed, result = choice_map.get(module.params['state'])(module.params)
	module.exit_json(changed=has_changed, meta=result)

if __name__ == '__main__':
	main()
