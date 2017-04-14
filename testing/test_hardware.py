#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tuesday April 11 15:29:17

@author: Hugh472
"""

import pytest
import yaml
import argparse
import os
import sys
import subprocess as sp

@pytest.fixture(scope='function', autouse=True)
def quads_init():
    args = Test_Hardware.quads + " --init --force"
    sp.call(args, shell=True)

    args = Test_Hardware.quads + " --define-cloud cloud01 --description cloud01"
    sp.call(args, shell=True)
 
    args = Test_Hardware.quads + "--move-hosts "
    sp.call(args, shell=True)

@pytest.fixture(scope='function')
def quads_config():
    pass

class Test_Hardware:
    quads = "../bin/quads.py"
   
    def test_quads_init_fail(self):
       
        args = Test_Hardware.quads + " --init"
        assert sp.call(args, shell=True) == 1

    def test_quads_init_pass(self):
       
        args = Test_Hardware.quads + " --init --force"
        assert sp.call(args, shell=True) == 0

    def test_move_hosts(self, quadsinstance, **kwargs):
	pass
       

	

