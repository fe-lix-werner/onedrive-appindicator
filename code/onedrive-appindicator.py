import gi
import os
import threading

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk

APPINDICATOR_ICON_ON = "/opt/onedrive-indicator/on.svg"
APPINDICATOR_ICON_OFF = "/opt/onedrive-indicator/off.png"
APPINDICATOR_ID = "onedrive-indicator"

class Indicator:
    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID,APPINDICATOR_ICON_OFF,appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(gtk.Menu())
        self.update_loop()
        gtk.main()

    def update_loop(self):
        threading.Timer(5.0, self.update_loop).start()
        if (self.get_onedrive_status() == 'active\n'):
            self.set_active_icon()
        else:
            self.set_inactive_icon()

    def quit(self,source):
        gtk.main_quit()

    def set_active_icon(self):
        self.indicator.set_icon_full(APPINDICATOR_ICON_ON,'')

    def set_inactive_icon(self):
        self.indicator.set_icon_full(APPINDICATOR_ICON_OFF,'')

    def get_onedrive_status(self):
        return os.popen('systemctl is-active --user onedrive.service').read()

def main():
    Indicator()

if __name__ == '__main__':
    main()

