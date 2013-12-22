#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic test classes for testing the geojson validator
"""
import os.path
from glob import glob
from itertools import chain

try:
    import simplejson as json
except ImportError:
    import json
import nose
from jsonschema import ValidationError

import geojsonvalidation

class TestGeoJSONValidation(object):

    @classmethod
    def setup_class(cls):
        """
        Load up the geojson to be checked
        """
        test_dir = os.path.abspath(os.path.dirname(__file__))

        def read_json(path):
            return json.load(open(path))

        cls.valid_geojson = map(
            read_json,
            glob(os.path.join(test_dir, "valid_geojson", "*.geojson"))
        )
        cls.invalid_geojson = map(
            read_json,
            glob(os.path.join(test_dir, "invalid_geojson", "*.geojson"))
        )


    @classmethod
    def teardown_class(cls):
        pass


    def _run_geojson_dict_is_valid(self, geojson):
        """
        Runner function that can be yielded as part of other tests.

        :param geojson: geojson to be validated
        :type geojson: dict
        :return: Is geojson valid
        :rtype: bool
        """
        return geojsonvalidation.geojson_dict_is_valid(geojson)


    def test_validation_runs(self):
        """
        Check the validation runs for all the read geojson
        """
        for gj in chain(self.valid_geojson, self.invalid_geojson):
            yield self._run_geojson_dict_is_valid, gj


    def _assert_valid(self, geojson, should_be_valid=True):
        """
        Assert whether or not the geojson should validate

        :param geojson: Geojson to validate
        :param should_be_valid: Whether or not the data should be valid
        :type should_be_valid: bool
        """
        assert self._run_geojson_dict_is_valid(geojson) == should_be_valid, "geojson != %r" % should_be_valid


    def test_all_valid_is_valid(self):
        """
        Test that all the valid geojsons are valid
        """
        for gj in self.valid_geojson:
            yield self._assert_valid, gj, True


    def test_all_invalid_is_invalid(self):
        """
        Test all the invalid geojsons correctly return as invalid
        """
        for gj in self.invalid_geojson:
            yield self._assert_valid, gj, False


    @nose.tools.raises(ValidationError)
    def _raise_errors_on_invalid(self, geojson):
        return geojsonvalidation.geojson_dict_is_valid(geojson, True)


    def test_invalid_raises(self):
        """
        Test that invalid schemas can still raise errors
        """
        for gj in self.invalid_geojson:
            yield self._raise_errors_on_invalid, gj


    def _get_dict_by_part_from_invalid(self, geojson):
        """
        Check that we're getting dictionaries back from broken geojson
        """
        assert isinstance(geojsonvalidation.validate_geojson_by_part(geojson), dict)

    def test_getting_dict_back_for_invalid(self):
        for gj in self.invalid_geojson:
            yield self._get_dict_by_part_from_invalid, gj


if __name__ == "__main__":
    nose.main()
