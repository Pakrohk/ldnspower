#!/bin/bash
#

# --check return command output error fun ---#
check_command() {
	command
	if [ $? -eq 0 ]; then
		return 0
	else
		return 1
	fi
}

#---------------------------------------------#

#------ grep active network interface --------#
active_device=$(nmcli -t -f device connection show --active)

#------ grep active network connection type --#
connection_type=$(nmcli -t -f type connection show --active)

#--- Checking the presence of an active interface connection ---#
check_command sudo nmcli con up $active_device >/dev/null 2>&1
if [ $? -eq 0 ]; then
	# --- Deleting the active connection ---#
	nmcli connection delete type $connection_type con-name $active_device >/dev/null 2>&1
	# ---- Creating a new connection with an active interface ---#
	sudo nmcli connection add type $connection_type con-name $active_device >/dev/null 2>&1
	# --- New connection activation ---#
	sudo nmcli con up $active_device >/dev/null 2>&1
else
	# ---- Activate the existing connection, if any --#
	sudo nmcli con up $active_device >/dev/null 2>&1
fi

cat <<EOF
 --==[ ===================================== ]==--
 --==[ Auto DNS changer by Pakrohk! V0.1     ]==--
 --==[ Contact me :                          ]==--
 --==[ T.me/@Packrohk                        ]==--
 --==[ ===================================== ]==--

 Which choice you wanna make?
 =================================================
     1. Changing DNS to Google's DNS.           
     2. Changing DNS to OpenDNS's DNS.
     3. Cangeing Dns to CloudFlare's DNS.
     4. Changing DNS to Comodo's DNS.           
     5. Changing DNS to Shecan's DNS.
     6. Changing DNS to Begzar's DNS.
     7. Changing DNS to ElTeam's Gameing DNS
 =================================================
EOF

read -p "Enter your desired DNS number : " DNS

NETNAME=$(nmcli -t -f NAME c show --active | head -n 1)

if [[ $DNS == 1 ]]; then
	sudo nmcli connection modify $NETNAME ipv4.dns "8.8.8.8 8.8.4.4"
	sudo nmcli connection modify $NETNAME ipv6.dns "2001:4860:4860::8888 2001:4860:4860::8844"
	sudo nmcli networking off
	sudo nmcli networking on
	sudo nmcli con up $active_device >/dev/null 2>&1
elif [[ $DNS == 2 ]]; then
	sudo nmcli connection modify $NETNAME ipv4.dns "208.67.222.222 208.67.220.220"
	sudo nmcli connection modify $NETNAME ipv6.dns " 2620:119:35::35 2620:119:53::53"
	sudo nmcli networking off
	sudo nmcli networking on
	sudo nmcli con up $active_device >/dev/null 2>&1
elif [[ $DNS == 3 ]]; then
	sudo nmcli connection modify $NETNAME ipv4.dns "1.1.1.1 1.0.0.1"
	sudo nmcli connection modify $NETNAME ipv6.dns "2606:4700:4700::1111 2606:4700:4700::1001"
	sudo nmcli networking off
	sudo nmcli networking on
	sudo nmcli con up $active_device >/dev/null 2>&1
elif [[ $DNS == 4 ]]; then
	sudo nmcli connection modify $NETNAME ipv4.dns "8.26.56.26 8.20.247.20"
	sudo nmcli connection modify $NETNAME ipv6.dns "0:0:0:0:0:FFFF:081A:381A 0:0:0:0:0:FFFF:0814:F714"
	sudo nmcli networking off
	sudo nmcli networking on
	sudo nmcli con up $active_device >/dev/null 2>&1
elif [[ $DNS == 5 ]]; then
	sudo nmcli connection modify $NETNAME ipv4.dns "178.22.122.100 185.51.200.2"
	sudo nmcli connection modify $NETNAME ipv6.method disabled
	sudo nmcli networking off
	sudo nmcli networking on
	sudo nmcli con up $active_device >/dev/null 2>&1
elif [[ $DNS == 6 ]]; then
	sudo nmcli connection modify $NETNAME ipv4.dns "185.55.226.26 185.55.225.25"
	sudo nmcli connection modify $NETNAME ipv6.method disabled
	sudo nmcli networking off
	sudo nmcli networking on
	sudo nmcli con up $active_device >/dev/null 2>&1
elif [[ $DNS == 7 ]]; then
	sudo nmcli connection modify $NETNAME ipv4.dns "78.157.42.100 78.157.42.101"
	sudo nmcli connection modify $NETNAME ipv6.method disabled
	sudo nmcli networking off
	sudo nmcli networking on
	sudo nmcli con up $active_device >/dev/null 2>&1
fi
