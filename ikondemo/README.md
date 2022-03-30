__This setup has been deprecated; use dm-ansible instead.__

This folder contains files relevent for the IKON13 demo in Utgård. The subfolder demoscripts/
contain bash scripts to start and stop EFU's and data generators along with some configuration
and (for multigrid) calibration files.

The root folder contains Ansible scripts to orchestrate the execution of the scripts and binaries
on the ESSIIP servers.

The scripts assume that detector data has already been copied to the servers and placed
in the ikondata/ folder.

After changing scripts or data files you need to deploy these changes to the servers

      > ansible-playbook -i utgard deployment.yml --ask-become-pass

To then start and stop the demo use the following commands

      > ansible-playbook -i utgard start_services.yml --ask-become-pass
      > ansible-playbook -i utgard stop_services.yml --ask-become-pass

Scripts for starting individual EFUs and data generators are in the action/ directory.
Detector types can be selected or excluded by using the `--tags` and `--skip-tags` options.
