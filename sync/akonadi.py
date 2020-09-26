#-*- coding: utf-8 -*-

""" Connect and use Akonadi

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2015-12-02
    Licence: GPL-2+
"""

import sys
import time
import logging
import subprocess
import os

from gi.repository import GObject as gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop

logger = logging.getLogger("AkonadiSync")
serverLog = logging.getLogger("Akonadi")

class AkonadiServer():
    """start/stop akonadi with enter/exit the with statement."""
    def __init__(self, stdout, stderr):
        """
        stdout: filehandle for stdout (is normaly empty for akonadi)
        stderr: filehandle for stderr (is full of the log of akonadi)
        """
        self.stdout = stdout
        self.stderr = stderr

    def __enter__(self):
        serverLog.info("starting akonadi ...")
        subprocess.Popen(["akonadictl", "start"], stdout = self.stdout, stderr = self.stderr)
    def __exit__(self, type, value, traceback):
        serverLog.info("stopping akonadi ...")
        os.system('akonadictl stop')
#        subprocess.Popen(["akonadictl", "stop"], stdout = self.stdout, stderr = self.stderr)
#        self.waitForEnd()

    def waitForEnd(self):
        """akonadi takes a while to shutdown, after stop is send"""
        status = "running"
        while status != "stopped":
            p = subprocess.Popen(["akonadictl", "status"], stderr=subprocess.PIPE)
            for line in p.stderr:
                if line.startswith(b'Akonadi Server: stopped'):
#                    status = line.split(":")[1].strip()
#                    if status == "stopped":
                    break
            time.sleep(1)


def fullSync(name):
    """Triggers a full Sync of a resource and blocks until it is done.

    name: a string of the resource f.ex: akonadi_kolab_resource_0
          you can find the resource from qdbusviewer org.freedesktop.Akonadu.Resource.<name>

    """

    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()

    def statusCallback(status, msg):
        logger.debug("%i: %s"%(status, msg))
        if status == 0:
            logger.info("status switched to idle on {}.".format(name))

    def synchronizedCallback():
        logger.info("fullSync for {} complete.".format(name))
        gobject.timeout_add(1, loop.quit)

    def warningCallback(msg):
        logger.info("Warning during sync: %s"%(msg))

    def errorCallback(msg):
        logger.info("Error during sync: %s"%(msg))

    timeout = 0
    while 1:
        try:
            proxy = session_bus.get_object('org.freedesktop.Akonadi.Resource.{}'.format(name), "/")
            break
        except dbus.exceptions.DBusException:
            time.sleep(1)
            timeout = timeout + 1
            if timeout >= 10:
                logger.critical("Failed to find the resource on dbus {}".format(name))
                sys.exit(-1)

    if not proxy.isOnline():
        proxy.setOnline(True)
        time.sleep(1)

    if not proxy.isOnline() or proxy.statusMessage() == u'Server is not available.':
           logger.critical("Kolab server is not available.")
           sys.exit(-1)

    proxy.connect_to_signal("status", statusCallback, dbus_interface="org.freedesktop.Akonadi.Agent.Status")
    proxy.connect_to_signal("synchronized", synchronizedCallback, dbus_interface="org.freedesktop.Akonadi.Resource")
    proxy.connect_to_signal("warning", warningCallback, dbus_interface="org.freedesktop.Akonadi.Agent.Status")
    proxy.connect_to_signal("error", errorCallback, dbus_interface="org.freedesktop.Akonadi.Agent.Status")
    proxy.synchronize(dbus_interface='org.freedesktop.Akonadi.Resource')

    logger.info("fullSync for {} started".format(name))

    loop = gobject.MainLoop()
    loop.run()
