# Copyright (C) 2009  Lars Wirzenius
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


import os

import obnamlib


class App(object):

    '''Main program for backup program.'''
    
    def __init__(self):
        self.hooks = obnamlib.HookManager()
        self.config = obnamlib.Configuration([])

        self.pm = obnamlib.PluginManager()
        self.pm.locations = [self.plugins_dir()]
        self.pm.plugin_arguments = (self,)

        self.hooks.new('plugins-loaded')
        self.hooks.new('shutdown')
        
    def plugins_dir(self):
        return os.path.join(os.path.dirname(obnamlib.__file__), 'plugins')
        
    def run(self):
        self.pm.load_plugins()
        self.pm.enable_plugins()
        self.hooks.call('plugins-loaded')
        self.config.load()
        print 'args:', self.config.args
        self.hooks.call('shutdown')
