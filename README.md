# Ansible roles for Ubuntu laptop or desktop install

**Note begin**: I am rebuilding this repository. What must be done:

- `vscode` **settings** must be rebuilt
- `wordlists` must be rebuilt
- example inventory  must be rebuilt

**Note end**.

This repository contains some roles meant to be used after a basic Ubuntu installation.
The defined roles are:

- `common` install the apps defined in `common_apps` and `group_apps` variables
- `clamav` installs clamav and freshclam then sets the number of checks per day
- `dconf`, see it's source for description of functionality
- `firewall` installs `nftables` and `firewalld`
- `git` installs `git` and sets it's global settings from the `git_global_options` variable
- `hydra` installs THC Hydra
- `keyboard` adds custom keyboard profiles / layouts. It contains keyboard layouts for converting a laptop keyboard to a **Tenkeyless**-like one, using the numberpad as navigation keys. See [this](https://calinradoni.github.io/pages/211101-laptoptenkeyless.html) post for details.
- `kicad` installs a `KiCad` version from it's ppa
- `nodejs` installs `Node.js` from `nodesource.com` repository
- `podman` installs `podman`, `buildah`, `slirp4netns` and `fuse-overlayfs`. In Ubuntu 20.04 uses the [Kubic project](https://build.opensuse.org/package/show/devel:kubic:libcontainers:stable/podman) provided packages. For other distributions uses the default repositories.
- `python` installs `python3`, `python3-pip` and `python3-venv`
- `ruby_bundler` installs `ruby-full` and `ruby-bundler`
- `setuser` sets basic user properties, see it's source for description of functionality
- `teams_insiders` installs `Teams Insiders` from Microsoft's repository
- `vim` installs `vim` and sets `/etc/vim/vimrc.local`
- `vscode` installs `Visual Studio Code` from Microsoft's repository, extensions and custom user settings. For extensions I have built an Ansible module.
- `wordlists` downloads wordlists into user's `~/wordlists` directory. Downloading is implemented from [SkullSecurity.org](https://wiki.skullsecurity.org/index.php/Passwords), [KaliLists/dirbuster](https://github.com/3ndG4me/KaliLists/tree/master/dirbuster) and from any complete URL.
- `zaproxy` installs OWASP ZAP using the official [ZAP Linux Repos](https://software.opensuse.org/download.html?project=home%3Acabelo&package=owasp-zap)

This is a *work-in-progress* and should be tested before use.

## About Ansible

You may start by reading [Ansible notes and quick start](https://calinradoni.github.io/pages/230129-ansible-notes-qs.html)

## Usage

On the control host (the local host if the roles will be launched from this host) run:

```sh
sudo apt update
sudo apt install software-properties-common
sudo apt install python3 python3-pip python3-venv python3-jmespath python3-psutil
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible ansible-lint

# install the requirements with
[[ -r requirements.yml ]] && ansible-galaxy collection install -r requirements.yml
# to upgrade all collections from a 'requirements.yml' file use:
# [[ -r requirements.yml ]] && ansible-galaxy collection install --upgrade -r requirements.yml
# or, to upgrade a single collection, use:
# ansible-galaxy collection install --upgrade <collection_name>
```

### With inventory file(s)

In the root directory of the repository create the `inventories/production` directory.
Inside the `inventories/production` directory copy the content of the `inventories/example` directory.

The default configuration files are `inventories/production/all.yml`, where you should put the common settings, and `inventories/production/desktops.yml` and `inventories/production/laptops.yml` for specific ones.

**Modify !** the files for your environment, mostly:

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

### Without inventory file

All needed variables must be passed on the command line.
Read [Defining variables at runtime](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#id37) for more information.

**Warning**: Some roles will not work if their variables are not set.

Here are some simple examples:

```sh
# run the playbook against localhost
ansible-playbook -i 127.0.0.1, \
    --become --ask-become-pass \
    -e 'ansible_connection=local' \
    -e 'local_user_name=your_user_name' \
    site.yml

# run the playbook against the remote host 192.168.5.123
ansible-playbook -i 192.168.5.123, \
    --become --ask-become-pass \
    -e 'local_user_name=your_user_name' \
    site.yml
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
