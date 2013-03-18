lizard-datasource
==========================================

Installation
============

"lizard_datasource" should be in installed apps, its urls should be
added to urls.py, and bin/django migrate should be run.

If you want to use datasources from other apps, e.g. from lizard-fewsjdbc,
then a recent enough version of lizard-fewsjdbc also needs to be installed.

The command 'bin/django cache_latest_values' should be setup to run every minute.
By default it doesn't cache anything (only values that are used are cached, and
you haven't added anything that will be used yet) but this also creates models
in the database that can be used to configured lizard-datasource.

To run it through supervisor in a buildout, add something like
this to buildout.cfg:

In [supervisor]:

      20 cache_latest_values (autostart=false autorestart=false startsecs=0) ${buildout:bin-directory}/django [cache_latest_values]

And then a latest-values-cronjob:

[latest-values-cronjob]
recipe = z3c.recipe.usercrontab
times = * * * * *
command = ${buildout:bin-directory}/supervisorctl start cache_latest_values > /dev/null

This script runs every minute, but it checks each datasource to see if
it is due yet. By default, the script is run 24 times per day (every
hour). This amount can be changed in the admin interface, and a single
run can also be request as an action.


Idea
====

This is a library that works as an abstraction layer between data
sources (of any kind, in principle, but mostly those that have
geographical locations and timeseries data), and frontend clients.

The following are main design ideas:
- Lizard-datasource tries to be as user-interface-agnostic as
  possible. It works with data and tries not to prejudice one
  type of user interface over another.

- Although there may be one or many data sources that
  lizard-datasource talks to at its backend, the interface presented
  to the frontend is always that of one single datasource.

- The one single datasource can be refined to a smaller subset by
  _choosing_ a value for some _criteria_, a type of facet search.
  Right now criteria either have a list of values or a tree structure
  of values, later on other types will be introduced too (like
  arbitrary numbers, or shapes of regions, or...)

- That said, not all data is of the same type. Some data has a small
  list of locations, some data is a 0.5m x 0.5m grid of a whole
  country. Some data sources can give a timeseries value for all its
  locations at any point in time very quickly, for others this isn't
  feasible at all, or only for the latest known value. Et cetera. In
  short, data sources have _properties_ and clients may choose to only
  receive data from data sources that have the properties they can
  deal with.

- Any list of locations or timeseries may have extra data associated
  with it, so-called _annotations_. These can be used for instance to
  give the locations different colors or icons, or to add percentiles
  or threshold values to timeseries. Lizard-datasource adds them as
  metadata and may give descriptions for them as a sort of legend, but
  the decision of what to do with them visually is left to the client.

- Abstract datasources can be defined, for instance an "augmented
  datasource" that takes an existing datasource and adds things to
  it. Lizard-datasource defines one. It can use data that some
  datasource yields if certain choices are made, and use it for
  annotations (colors, percentiles) when other choices are made.

To connect a new type of datasource to lizard-datasource, implement a
subclass of lizard_datasource.datasource.DataSource, and make it
available by the entry_points mechanism; as an example, see
lizard_datasource's setup.py to see how its own datasources are
included. They should point to a factory function that returns a list
of datasource instances.

Clients of lizard-datasource use the
lizard_datasource.datasource.datasource() function to get a datasource
instance (possibly with a choices_made argument to refine the
data). It can then use the functions of the DataSource class to draw a
map or a graph, or just send a lot of numbers to the line printer.
