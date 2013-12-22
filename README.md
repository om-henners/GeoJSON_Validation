# GeoJSON_Validation

Validate GeoJSON with the JSON-schema specification

This requires the [jsonschema](http://python-jsonschema.readthedocs.org) package.

## Usage

There are two main functions which both require the GeoJSON to be read as a Python dictionary. If the geojson can't be
read into a Python dictionary then the data is invalid anyway. Note that when the package is imported it automatically
loads the schema into memory to avoid having to reload each time a scan is done. The schema itself is small so this
shouldn't be a big issue.

    geojson_dict_is_valid(geojson[, raise_on_error=False])

This will simply return a `True` or `False` whether the GeoJSON is valid or not. Optionally if `raise_on_error` is
`True` a `jsonschema.ValidationError` will be raised.

    validate_geojson_by_part(geojson)

This function is designed more for actual diagnostics. It will iterate over the GeoJSON object from the lowest level
and return the first invalid part of the schema it can find. If the schema is valid it will return `None`. To fully fix
a large GeoJSON schema this may have to be run multiple times.