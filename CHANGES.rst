Changelog of lizard-datasource
===================================================


0.9 (unreleased)
----------------

- Fix #4, which was partly due to AugmentedDataSource.unit() not
  accepting calls without argument, and partly due to bad
  configuration. Added and fixed tests.


0.8.1 (2013-04-11)
------------------

- Forgot to add the migration for unit_cache.


0.8 (2013-04-11)
----------------

- Add a 'unit_cache' field to datasource layer, so that it doesn't
  have to be retrieved from FEWS etc all the time, and so that it can
  be edited in the admin.

- Let the cache_latest_values script also fill the unit_cache.

- Do not set a default color in lizard-datasource if there is no
  coloring, leave that to frontend apps.

- Use layer units as column names for DataFrames. Keep track of the right order
  of column names, because DateFrame doesn't.


0.7 (2013-04-10)
----------------

- Change Timeseries object so that it can contain multiple timeseries.

- Add an ExtraGraphLine possibility to AugmentedDatasource so that it
  can return multiple-valued timeseries.

- Create IdentifierMappings because the IDs of both layers may not
  match.

- Create ProximityMappings, automatically created IdentifierMappings based
  on matching locations to the closests locations in the other layer.

- Call a script to create these from the admin interface.

- Give nicknames to DatasourceLayers, and only choose from nicknames
  when configuring ColorFromLatestValue, PercentileLayer or
  ExtraGraphLine options.

- Fix a bug in running the cache_latest_values script -- the stored datetime
  at which the script last ran was stored timezone-aware, but the calculations
  weren't, which led to an exception.

- Only create proximity mappings if a match is found within some
  maximum distance.


0.6 (2013-03-19)
----------------

- If the cache_latest_values script runs every minute, it is now possible
  to active it so that it will work next minute using the admin interface.

- It is now possible to configure the number of times the cache script
  activates that way per day.

- Improve the datasource model admin pages



0.5 (2013-03-05)
----------------

- Fix bug where a combined datasource for which no choices were made
  yet did not get an empty choices made object.


0.4.1 (2013-02-12)
------------------

- Nothing changed yet.


0.4 (2013-02-12)
----------------

- Add new 'location_annotations' method to a datasource. It gives a list
  of possible annotations that this datasource gives to its locations
  (e.g., a color) and possible also gives some legend information for
  the annotations.

- Added description fields to colormaps so that they can have a good
  legend, added descriptions like "0 <= x < 1" using the colormap's
  boundaries if there are no descriptions.

- Augmented datasource implements location_annotations using the
  colormap's legend.


0.3 (2013-01-16)
----------------

- Removed hardcoding of options.

- The cache script now creates all layer objects, but only downloads
  values for layers of which the latest value is used by something
  (coloring).

- Coloring is done using the configuration in the ColorFromLatestValue
  model.

- Percentile bars are done using the configuration in the
  PercentileLayer model.

- Layers that are used for augmenting other layers (color layers,
  percentile layers) can now be hidden.

- Add a 'visible_criteria' method to datasources, that by default just
  returns chooseable_criteria(). This should be used to hide choices
  that shouldn't be shown to the user. The previous method of hiding
  them from visible_criteria was inadequate, because then they would
  be hidden from internal use too (e.g., the caching script couldn't
  find them either).

- Add a 'unit' method to datasources, that optionally returns a string
  describing the unit of the data represented by them.


0.2 (2012-12-20)
----------------

- Implemented support for percentiles added by
  augmented_datasource.py. Not dynamic yet.

- Implemented colors from 'klasse' parameter. Also not configurable
  yet.

0.1.1 (2012-11-15)
------------------

Renamed package to lizard-datasource instead of lizard_datasource,
because everything else follows that scheme too.


0.1 (2012-11-15)
----------------

Code doesn't really function yet, but we need a test release of the
grondwaterinbrabant site. CHANGES will be kept up to date from here
on.
