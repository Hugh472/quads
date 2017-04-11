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

@pytest.fixture
def quads_init():
	pass

@pytest.fixture
def quads_config():
	pass

class Test_Hardware:
	quads = "../bin/quads.py"

	def test_move_hosts(self, quadsinstance, **kwargs):
		pass

