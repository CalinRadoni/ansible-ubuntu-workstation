# Ansible roles for Ubuntu laptop or desktop install

This repository contains some roles meant to be used after a basic Ubuntu installation.
The defined roles are:

- `common` install the apps defined in `common_apps` and `group_apps` variables
- `dconf`, see it's source for description of functionality
- `firewall` installs `nftables` and `firewalld`
- `git` installs `git` and sets it's global settings from the `git_global_options` variable
- `keyboard` adds custom keyboard profiles. It contains keyboard profiles for converting *standard* laptop keyboard to a **Tenkeyless** one, basically converting the numberpad to navigation keys.
- `nodejs` installs `Node.js` from `nodesource.com` repository
- `python` installs `python3-pip` and `python3-venv`
- `ruby` installs `ruby-full` and `ruby-bundler`
- `setuser` sets basic user properties, see it's source for description of functionality
- `teams` installs `Teams` from Microsoft's repository
- `vim` installs `vim` and sets `/etc/vim/vimrc.local`
- `vscode` installs `Visual Studio Code` from Microsoft's repository

This is a *work-in-progress* and should be tested before use.

## Usage

On the control host (the local host if the roles will be launched from this host) run:

```sh
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible

# install the requirements with
ansible-galaxy collection install -r requirements.yml
# upgrade the requirements with
#ansible-galaxy collection install <collection_name> --upgrade
```

In the root directory of the repository create the `inventories/production` directory.
Inside the `inventories/production` directory copy the content of the `inventories/example` directory.

The default configuration files are `inventories/production/all.yml`, where you should put the common settings, and `inventories/production/desktops.yml` and `inventories/production/laptops.yml` for specific ones.

**Modify** the files for your environment, mostly:

- `local_user_name` should be the name of your standard user;
- set the content of `git_global_options` as needed;
- enable the roles that you want in `site.yml`.

Then, for *production* environment, use:

```sh
# if configuring a laptop
ansible-playbook --ask-become-pass -i inventories/production --limit laptop_local site.yml

# if configuring a desktop
ansible-playbook --ask-become-pass -i inventories/production --limit desktop_local site.yml
```

## Development

When using [Visual Studio Code](https://code.visualstudio.com/) as editor, add the [Ansible VS Code Extension by Red Hat](https://marketplace.visualstudio.com/items?itemName=redhat.ansible) and install [Ansible Lint](https://ansible-lint.readthedocs.io/en/latest/):

```sh
sudo python3 -m pip install ansible-lint
```

### Python modules

`cd` to the root directory of the repository and create a python virtual environment:

```sh
[ ! -d .venv ] && python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install psutil
deactivate
```

To test `vscode_extension_installer.py` :

```sh
# activate the venv
source .venv/bin/activate

# create a file to pass arguments to the vscode_extension_installer module
mkdir -p tmp
cat << 'EOF' > tmp/test_args.json
{
    "ANSIBLE_MODULE_ARGS": {
        "name": "redhat.ansible"
    }
}
EOF

# test the vscode_extension_installer module
python roles/vscode/library/vscode_extension_installer.py tmp/test_args.json
```

## License

This repository is licensed under the terms of [GNU GPLv3](http://www.gnu.org/licenses/gpl-3.0.html) license. See the `LICENSE-GPLv3.txt` file.