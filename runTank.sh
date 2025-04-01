#sudo nmcli  device wifi hotspot con-name  "BLITZTANK" ssid "BLITZTANK" password blitz ifname wlan0
nmcli connection add type wifi con-name "BLITZTANK" ssid "BLITZTANK" mode ap ipv4.method shared wifi-sec.key-mgmt none


#Confirm a Static IP on BLITZTANK Hotspot
sudo nmcli connection modify BLITZTANK ipv4.addresses 192.168.69.69/24

