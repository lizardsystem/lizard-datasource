Changelog of lizard-datasource
===================================================


0.3 (unreleased)
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
