
This folder contains files relevent for the IKON13 demo in Utgård. The subfolder demoscripts/
contain bash scripts to start and stop EFU's and data generators along with some configuration
and (for multigrid) calibration files.

The root folder contains Ansible scripts to orchestrate the execution of the scripts and binaries
on the ESSIIP servers.

The scripts assume that detector data has already been copied to the servers and placed
in the ikondata/ folder.

After changing scripts or data files you need to deploy these changes to the servers

      > ansible-playbook -i essiip-lab deployment.yml --ask-become-pass
      > ansible-playbook -i essiip-lab sonde_deployment.yml --ask-become-pass

To then start and stop the demo use the following commands

      > ansible-playbook -i essiip-lab start_services.yml --ask-become-pass
      > ansible-playbook -i essiip-lab stop_services.yml --ask-become-pass

Scripts for starting individual EFUs and data generators are in te action/ directory.
