import gi
import os
import threading

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk

from enum import Enum, auto

APPINDICATOR_ICON_ON = "/opt/onedrive-indicator/on.svg"
APPINDICATOR_ICON_OFF = "/opt/onedrive-indicator/off.svg"
APPINDICATOR_ICON_UP = "/opt/onedrive-indicator/up.svg"
APPINDICATOR_ICON_DOWN = "/opt/onedrive-indicator/down.svg"

APPINDICATOR_ID = "onedrive-indicator"
LAST_JOURNAL_LINE_COMMAND = "journalctl --user-unit onedrive | grep 'Uploading\|Downloading' | tail -n 1"

class Indicator:
    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID,APPINDICATOR_ICON_OFF,appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(gtk.Menu())
        self.update_loop()
        gtk.main()

    def update_loop(self):
        threading.Timer(3.0, self.update_loop).start()
        status = self.get_status()
        if status == Status.INACTIVE:
            self.set_inactive_icon()
        elif status == Status.ACTIVE:
            self.set_active_icon()
        elif status == Status.DOWNLOADING:
            self.set_downloading_icon()
        else:
            self.set_uploading_icon()
        print(status)


    def set_uploading_icon(self):
        self.indicator.set_icon_full(APPINDICATOR_ICON_UP,'')

    def set_downloading_icon(self):
        self.indicator.set_icon_full(APPINDICATOR_ICON_DOWN,'')

    def set_active_icon(self):
        self.indicator.set_icon_full(APPINDICATOR_ICON_ON,'')

    def set_inactive_icon(self):
        self.indicator.set_icon_full(APPINDICATOR_ICON_OFF,'')

    def get_status(self):
        if (self.get_onedrive_process_status() == Status.INACTIVE):
            return Status.INACTIVE
        return self.get_status_from_journal_log()


    def get_onedrive_process_status(self):
        process = os.popen('systemctl is-active --user onedrive.service')
        process_output = process.read()
        process.close()
        if (process_output == 'active\n'):
            return Status.ACTIVE
        return Status.INACTIVE

    def get_status_from_journal_log(self):
        process = os.popen(LAST_JOURNAL_LINE_COMMAND)
        process_output = process.read()
        process.close()
        if "done" in process_output:
            return Status.ACTIVE
        if "Uploading" in process_output:
            return Status.UPLOADING
        return Status.DOWNLOADING


class Status(Enum):
    ACTIVE = 1
    INACTIVE = 2
    UPLOADING = 3
    DOWNLOADING = 4

def main():
    Indicator()

if __name__ == '__main__':
    main()

