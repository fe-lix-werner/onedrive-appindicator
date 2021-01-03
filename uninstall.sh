remove_indicator()
{
    # Stop Service
		echo"Stopping the service"
		systemctl stop --user onedrive-indicator.service

		# Installing indicator in opt directory
    echo "Removing OneDrive Indicator"
    sudo rm -rf /opt/onedrive-indicator/

    # Installing autostart desktop file
    echo "Removing Onedrive Indicator service"
    rm $HOME/.config/systemd/user/onedrive-indicator.service

}

remove_indicator
