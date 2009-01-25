# Copyright (C) 2008  Lars Wirzenius <liw@liw.fi>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import obnamlib


class FileContents(obnamlib.Object):

    """Store the full contents of a file."""

    kind = obnamlib.FILECONTENTS

    def __init__(self, id):
        obnamlib.Object.__init__(self, id=id)

    @property
    def part_ids(self):
        return self.find_strings(kind=obnamlib.FILEPARTREF)

    def add(self, ref):
        c = obnamlib.Component(kind=obnamlib.FILEPARTREF, string=ref)
        self.components.append(c)