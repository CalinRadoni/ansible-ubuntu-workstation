#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Calin Radoni (https://github.com/CalinRadoni)
# Based on: https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: vscode_extension_installer
short_description: This module installs a Visual Studio Code extension
description:
  - This module installs a Visual Studio Code extension if is not installed.
version_added: "1.0.0"
author: "Calin Radoni (https://github.com/CalinRadoni)"
options:
  name:
    description:
      - This is the name of the extension to be installed.
      - Use the full extension name, for example 'ms-python.python'.
    required: true
    type: str
seealso:
  - name: Module format and documentation
    link: https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html
  - name: AnsibleModule
    link: https://docs.ansible.com/ansible/latest/reference_appendices/module_utils.html
'''

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule


def install_extension(module, name):
    rc, cmd_out, cmd_err = module.run_command(['code', '--install-extension', name])
    if rc != 0 :
        print('Error')
        module.fail_json(msg = 'Failed to install extension %s: %s %s' % (name, cmd_out, cmd_err))

    return 'successfully installed' in cmd_out


def run_module():
    module_args = dict(
        name = dict(type = 'str', required = True)
    )

    result = dict(
        changed = False,
        original_message = '',
        message = ''
    )

    module = AnsibleModule(argument_spec = module_args, supports_check_mode = False)

    name = module.params['name']

    result['original_message'] = name

    if install_extension(module, name):
        result['message'] = 'successfully installed'
        result['changed'] = True
    else:
        result['message'] = 'already installed'
        result['changed'] = False

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
