#!/bin/sh
show_menu(){
    normal=`echo "\033[m"`
    menu=`echo "\033[36m"` #Blue
    number=`echo "\033[33m"` #yellow
    bgred=`echo "\033[41m"`
    fgred=`echo "\033[31m"`
    printf "\n${menu}********************************************* ${normal}\n"
    printf "${menu}**${number} 0)${menu} Open VIP demo checklist ${normal}\n"
    printf "${menu}**${number} 1)${menu} Check Kafka server status ${normal}\n"
    printf "${menu}**${number} 2)${menu} Deploy EFUs ${normal}\n"
    printf "${menu}**${number} 3)${menu} Check if Kafka is running ${normal}\n"
    printf "${menu}**${number} 4)${menu} Not implemented ${normal}\n"
    printf "${menu}**${number} 5)${menu} Deploy/start Forwarder, FileWriter, Graphite, Grafana ${normal}\n"
    printf "${menu}**${number} 6)${menu} Not implemented ${normal}\n"
    printf "${menu}**${number} 7)${menu} Not implemented ${normal}\n"
    printf "${menu}**${number} 8)${menu} Not implemented ${normal}\n"
    printf "${menu}**${number} 9)${menu} Open Graylog (admin/password) ${normal}\n"
    printf "${menu}**${number} 9b)${menu} Open Grafana dashboards ${normal}\n"
    printf "${menu}**${number} 10)${menu} Start EFU and data generators ${normal}\n"
    printf "${menu}**${number} 11)${menu} Not implemented ${normal}\n"
    printf "${menu}**${number} 12)${menu} Not implemented ${normal}\n"
    printf "${menu}**${number} 13)${menu} Not implemented ${normal}\n"
    printf "${menu}**${number} 14)${menu} Not implemented ${normal}\n"
    printf "${menu}**${number} 15)${menu} Stop EFUs and data generators ${normal}\n"
    printf "${menu}*********************************************${normal}\n"
    printf "Please enter a menu option and enter or ${fgred}x to exit. ${normal}"
    read opt
}

option_picked(){
    msgcolor=`echo "\033[01;31m"` # bold red
    normal=`echo "\033[00;00m"` # normal white
    message=${@:-"${normal}Error: No message passed"}
    printf "${msgcolor}${message}${normal}\n"
}
#
#
#

dmansiblepath=${DMANSIBLEDIR:-../../}
vaultfile=${VAULTFILE:-~/.vault_pass.txt}
dmansible=$dmansiblepath/dm-ansible


if ! [ -d $dmansible ]; then
  echo "can't cd into dm-ansible: ($dmansible) does not exist"
  echo "fix:"
  echo "  if dm-ansible/ is located in /home/zorro"
  echo "  export DMANSIBLEDIR=/home/zorro/"
  exit 1
fi

if ! [ -f $vaultfile ]; then
  echo "Ansible vault file ($vaultfile) doesn't exist"
  echo "fix:"
  echo "  if vaultfile is /home/zorro/myansible.txt"
  echo "  export VAULTFILE=fullpathname"
  exit 1
fi

echo "Ansible directory: $dmansible"
echo "Ansible vault    : $vaultfile"

#
#
#
clear
echo "Ansible directory: $dmansible"
echo "Ansible vault    : $vaultfile"
show_menu
while [[ $opt != '' ]]
    do
    if [[ $opt = '' ]]; then
      exit;
    else
      case $opt in
        0) clear;
            option_picked "Open VIP demo checklist";
            open "https://confluence.esss.lu.se/display/ECDC/VIP+Demo+Days"
            show_menu;
        ;;
        1) clear;
            option_picked "Check Kafka server status";
            open "http://dmsc-services01.cslab.esss.lu.se:3000/d/mRMCq2Cik/utgard-overview?orgId=1&refresh=30s"
            show_menu;
        ;;
        2) clear;
            option_picked "Deploy EFUs";
            ansible-playbook --inventory utgard --ask-become-pass deployment.yml
            printf "press enter to continue..."
            read nothing
            clear
            show_menu;
        ;;
        3) clear;
            option_picked "Check if Kafka is running";
            open "http://dmsc-services01.cslab.esss.lu.se:9001/clusters/utgard"
            show_menu;
        ;;
        5) clear;
            option_picked "Deploy/start Forwarder, FileWriter, Graphite, Grafana";
            pushd $dmansible
            ansible-playbook --vault-password-file $vaultfile --inventory inventories/utgard --ask-become-pass --forks 10 site.yml
            popd
            show_menu;
        ;;
        9) clear;
            option_picked "Open Graylog (admin/password)";
            open "http://dmsc-services01.cslab.esss.lu.se:9000/search?rangetype=relative&fields=message%2Csource&width=1827&highlightMessage=&relative=7200&q=message%3A%20%22detector%22%20OR%20message%3A%20%22Starting%20Event%20Formation%22"
            show_menu;
        ;;
        10) clear;
            option_picked "Start EFU and data generators";
            ansible-playbook -i utgard start_services.yml --skip-tags=generator
            printf "press enter to continue..."
            read nothing
            clear
            show_menu;
        ;;
        15) clear;
            option_picked "Stop EFUs and data generators";
            ansible-playbook -i utgard stop_services.yml --skip-tags=generator
            printf "press enter to continue..."
            read nothing
            clear
            show_menu;
        ;;
        9b) clear;
            option_picked "Open Grafana dashboards";
            open "http://dmsc-services01.cslab.esss.lu.se:3000/d/YQicRrKZk/multiblade?orgId=1&refresh=5s"
            open "http://dmsc-services01.cslab.esss.lu.se:3000/d/mvTZWHOZk/multigrid-mesytec-sns?orgId=1&refresh=5s"
            open "http://dmsc-services01.cslab.esss.lu.se:3000/d/rvSzZNdWk/gdgem-srs-new?orgId=1&refresh=5s"
            show_menu;
        ;;
        x)exit;
        ;;
        \n)exit;
        ;;
        *)clear;
            option_picked "Pick an option from the menu";
            show_menu;
        ;;
      esac
    fi
done
