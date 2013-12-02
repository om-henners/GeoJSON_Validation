#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base methods for GeoJSON Schema validation. Imported directly to the init of the module.
"""

try:
    import simplejson as json
except ImportError:
    import json

import jsonschema


