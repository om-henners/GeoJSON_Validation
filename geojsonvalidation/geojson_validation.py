#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base methods for GeoJSON Schema validation. Imported directly to the init of the module.
"""

#std lib
import os.path
import logging

#3rd party
try:
    import simplejson as json
except ImportError:
    import json
import jsonschema #http://python-jsonschema.readthedocs.org/en/latest/


_schema_home = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__)
    ),
    "schemas",
    "geojson"
)
_logger = logging.getLogger("GeoJSON Validation")


def __build_geojson_schema():
    """
    Build the jsonschema Draft4Validator object that is used to validate incoming GeoJSON.

    :return: jsonschema.Draft4Validator
    """
    geojson_base = json.load(
        open(
            os.path.join(
                _schema_home,
                "geojson.json"
            )
        )
    )

    #pre-cache the associated schema data so that we don't have to connect to the the given URLs (which don't exist)
    cached_json = {
        "http://json-schema.org/geojson/crs.json": json.load(open(os.path.join(_schema_home, "crs.json"))),
        "http://json-schema.org/geojson/bbox.json": json.load(open(os.path.join(_schema_home, "bbox.json"))),
        "http://json-schema.org/geojson/geometry.json": json.load(open(os.path.join(_schema_home, "geometry.json"))),
    }
    resolver = jsonschema.RefResolver(
        "http://json-schema.org/geojson/geojson.json",
        geojson_base,
        store=cached_json
    )

    return jsonschema.Draft4Validator(geojson_base, resolver=resolver)

#Instantite when the module loads, so on functions where we split up the geojson objects we don't need to reload the
#schema all the time
__VALIDATOR = __build_geojson_schema()

def __validate_geojson(geojson):
    """
    Validate a chunk of geojson. Used by the other functions to do the actual processing

    :raises: jsonschema.ValidationError
    """
    try:
        __VALIDATOR.validate(geojson)
    except jsonschema.ValidationError:
        _logger.exception("GeoJSON failed to validate")
        raise


def geojson_dict_is_valid(geojson):
    """
    Validate a geojson dictionary against the GeoJSON schema

    :rtype: bool
    """
    _logger.debug("Validating geojson dict")
    try:
        __validate_geojson(geojson)
        return True
    except jsonschema.ValidationError:
        return False


def validate_geojson_by_part(geojson):
    """
    Validate the geojson by part. Generates broken geojson segments at the lowest level possible. I.E if there is a
    feature within the feature collection that may be broken, return the feature instead.

    :return: generator
    """
    try:
        __validate_geojson(geojson)
    except jsonschema.ValidationError:
        try:
            if geojson["type"] == "GeometryCollection":
                for gj in geojson["geometries"]:
                    yield validate_geojson_by_part(gj)
            if geojson["type"] == "FeatureCollection":
                for gj in geojson["features"]:
                    yield validate_geojson_by_part(gj)
            if geojson["type"] == "Feature":
                yield geojson
        except KeyError:
            yield geojson