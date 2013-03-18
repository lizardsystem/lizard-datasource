Changelog of lizard-datasource
===================================================


0.6 (unreleased)
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
