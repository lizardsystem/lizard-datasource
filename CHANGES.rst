Changelog of lizard-datasource
===================================================


0.4 (unreleased)
----------------

- Nothing changed yet.


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
