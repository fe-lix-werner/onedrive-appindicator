

install_deps()
{
    # Install gir1.2-appindicator
    echo "Installing AppIndicator and Python-GI"
    sudo apt-get install -y gir1.2-appindicator python3-gi
}

install_indicator()
{
    # Installing indicator in opt directory
    echo "Installing Onedrive Indicator"
    sudo mkdir -p /opt/onedrive-indicator/
    sudo cp code/* /opt/onedrive-indicator/

    # Installing autostart desktop file
    echo "Installing Onedrive Indicator service"
    cp onedrive-indicator.service $HOME/.config/systemd/user/

		# Starting the service
		systemctl start --user onedrive-indicator.service
}

install_deps
install_indicator
