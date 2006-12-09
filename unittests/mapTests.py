# Copyright (C) 2006  Lars Wirzenius <liw@iki.fi>
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


"""Unit tests for obnam.map."""


import unittest


import obnam


class ObjectMappingTests(unittest.TestCase):

    def testEmpty(self):
        m = obnam.map.create()
        self.failUnlessEqual(obnam.map.count(m), 0)

    def testGetNonexisting(self):
        m = obnam.map.create()
        self.failUnlessEqual(obnam.map.get(m, "pink"), None)

    def testAddOneMapping(self):
        m = obnam.map.create()
        obnam.map.add(m, "pink", "pretty")
        self.failUnlessEqual(obnam.map.count(m), 1)
        
        self.failUnlessEqual(obnam.map.get(m, "pink"), "pretty")

    def testAddTwoMappings(self):
        m = obnam.map.create()
        obnam.map.add(m, "pink", "pretty")
        self.failUnlessRaises(AssertionError, obnam.map.add,
                              m, "pink", "beautiful")

    def testGetNewMappings(self):
        m = obnam.map.create()
        self.failUnlessEqual(obnam.map.get_new(m), [])
        obnam.map.add(m, "pink", "pretty")
        self.failUnlessEqual(obnam.map.get_new(m), ["pink"])
        obnam.map.reset_new(m)
        self.failUnlessEqual(obnam.map.get_new(m), [])
        obnam.map.add(m, "black", "beautiful")
        self.failUnlessEqual(obnam.map.get_new(m), ["black"])

    def testMappingEncodings(self):
        # Set up a mapping
        m = obnam.map.create()
        
        # It's empty; make sure encoding new ones returns an empty list
        list = obnam.map.encode_new(m)
        self.failUnlessEqual(list, [])

        # Add a mapping
        obnam.map.add(m, "pink", "pretty")

        # Encode the new mapping, make sure that goes well
        list = obnam.map.encode_new(m)
        self.failUnlessEqual(len(list), 1)
        
        # Make sure the encoding is correct
        list2 = obnam.cmp.decode_all(list[0], 0)
        self.failUnlessEqual(len(list2), 1)
        self.failUnlessEqual(obnam.cmp.get_kind(list2[0]), 
                             obnam.cmp.OBJMAP)
        
        list3 = obnam.cmp.get_subcomponents(list2[0])
        self.failUnlessEqual(len(list3), 2)
        self.failUnlessEqual(obnam.cmp.get_kind(list3[0]),
                             obnam.cmp.BLOCKREF)
        self.failUnlessEqual(obnam.cmp.get_string_value(list3[0]),
                             "pretty")
        self.failUnlessEqual(obnam.cmp.get_kind(list3[1]),
                             obnam.cmp.OBJREF)
        self.failUnlessEqual(obnam.cmp.get_string_value(list3[1]),
                             "pink")

        # Now try decoding with the official function
        block = obnam.map.encode_new_to_block(m, "black")
        m2 = obnam.map.create()
        obnam.map.decode_block(m2, block)
        self.failUnlessEqual(obnam.map.count(m2), 1)
        self.failUnlessEqual(obnam.map.get(m2, "pink"), "pretty")
