# Copyright 2016  Lars Wirzenius
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
#
# =*= License: GPL-3+ =*=


class LeafStoreInterface(object):  # pragma: no cover

    def put_leaf(self, leaf):
        raise NotImplementedError()

    def get_leaf(self, leaf_id):
        raise NotImplementedError()


class InMemoryLeafStore(LeafStoreInterface):

    def __init__(self):
        self._leaves = {}
        self._counter = 0

    def put_leaf(self, leaf):
        self._counter += 1
        self._leaves[self._counter] = leaf
        return self._counter

    def get_leaf(self, leaf_id):
        return self._leaves.get(leaf_id, None)
