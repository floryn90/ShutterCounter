# window.py
#
# Copyright 2020 Florin Lungu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk
from gi.repository import Gio, GObject
import gphoto2 as gp
import subprocess

@Gtk.Template(resource_path='/org/floryn90/shuttercounter/window.ui')
class ShuttercounterWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ShuttercounterWindow'
    window = ''
    camera_model_name = Gtk.Template.Child()
    shutter_counter_number = Gtk.Template.Child()
    camera_serial_number = Gtk.Template.Child()
    btn_update = Gtk.Template.Child()

    def get_camera_serial():
        camera = gp.Camera()
        hasCamInited = False
        camera_serial = ''
        try:
            camera.init()
            hasCamInited = True
        except Exception as ex:
            lastException = ex
            print("No camera: {} {}; ".format( type(lastException).__name__, lastException.args))
        if hasCamInited:
            camera_config = camera.get_config()
            # get the camera model
            OK, camera_serial = gp.gp_widget_get_child_by_name(
                camera_config, 'serialnumber')
            if OK < gp.GP_OK:
                OK, camera_serial = gp.gp_widget_get_child_by_name(
                    camera_config, 'serialnumber')
            if OK >= gp.GP_OK:
                camera_serial = camera_serial.get_value()
            else:
                camera_serial = ''
        return camera_serial

    def get_camera_model():
        camera = gp.Camera()
        hasCamInited = False
        camera_model = ''
        try:
            camera.init()
            hasCamInited = True
        except Exception as ex:
            lastException = ex
            print("No camera: {} {}; ".format( type(lastException).__name__, lastException.args))
        if hasCamInited:
            camera_config = camera.get_config()
            # get the camera model
            OK, camera_model = gp.gp_widget_get_child_by_name(
                camera_config, 'cameramodel')
            if OK < gp.GP_OK:
                OK, camera_model = gp.gp_widget_get_child_by_name(
                    camera_config, 'model')
            if OK >= gp.GP_OK:
                camera_model = camera_model.get_value()
            else:
                camera_model = ''
        return camera_model

    def get_camera_shutter():
        camera = gp.Camera()
        hasCamInited = False
        camera_shutter = ''
        try:
            camera.init()
            hasCamInited = True
        except Exception as ex:
            lastException = ex
            print("No camera: {} {}; ".format( type(lastException).__name__, lastException.args))
        if hasCamInited:
            camera_config = camera.get_config()
            # get the camera shutter counts
            OK, camera_shutter = gp.gp_widget_get_child_by_name(
                camera_config, 'shuttercounter')
            if OK >= gp.GP_OK:
                camera_shutter = camera_shutter.get_value()
            else:
                camera_shutter = ''
        return camera_shutter

    def update_camera_info(self):
        print("triggered")
        subprocess.run(["gio", "mount", "-s", "gphoto2"])
        camera_model = ShuttercounterWindow.get_camera_model()
        camera_serial = ShuttercounterWindow.get_camera_serial()
        shutter_count = ShuttercounterWindow.get_camera_shutter()

        ShuttercounterWindow.window.camera_model_name.set_label(camera_model)
        print("Camera Model => {}".format(camera_model))
        ShuttercounterWindow.window.camera_serial_number.set_label(camera_serial)
        print("Camera serial number => {}".format(camera_serial))
        ShuttercounterWindow.window.shutter_counter_number.set_label(shutter_count)
        print("Camera shutter count => {}".format(shutter_count))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ShuttercounterWindow.window = self
        self.btn_update.connect("clicked", ShuttercounterWindow.update_camera_info)

        
