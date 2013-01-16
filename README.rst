lizard-datasource
==========================================

This is a library that defines a layer that goes between data sources
(of any kind, in principle), and the frontend of Lizard apps. The
mechanism used to do so is reminiscent of adapters as defined by
lizard-map, but the datasource objects are entirely data-minded and
independent of any user interface.

An example of a data source is a FEWS server. There is an existing
Lizard app, lizard-fewsjdbc, that talks to a FEWS server over JDBC and
shows the results in Lizard. The user interface details are thus
directly coupled to the backend; a feature in the frontend that is
programmed for FEWS over JDBC will not work for other data sources.

Using this library however, lizard-fewsjdbc implements a subclass of
lizard_datasource.datasource.DataSource, which defines how to get at
the data in the FEWS server in a somewhat standardized
way. Lizard-datasource then combines all the available data sources in
the system, and presents them all as one combined datasource to the
outside world. Software talking to this combined datasource doesn't
know where the data is coming from and therefore can't couple with the
source of the data too tightly.

Lizard-fancylayers is a new Lizard app that shows data from
lizard-datasource. It should also be easy to write scripts that use
lizard-datasource, or a REST API, or many different Lizard apps for
different uses than the rather generic lizard-fancylayers. If
lizard-datasource will support other data types in the future (like
grids, or continuous data, or time dependent data, or datapoint of
which the values are not timeseries), then lizard-fancylayers may
choose not to support those; other apps will, it is not necessary that
each app that uses the data from lizard-datasource be able to deal
with all types.

However, as of today, only one type of data is implemented: data with
a finite number of discrete point locations that can be shown as
points on a map, and timeseries data at those locations.

Another possibility that naturally arises out of the existence of the
lizard-datasource layer is that of purely abstract data sources; data
sources that do not get their data from databases or such, but from
other data sources or from as-necessary computation. One such is
included: the AugmentedDataSource can take an existing data source,
and augment it. For instance, it can use values from some of the data
source's layers to color locations in other locations, or use some the
timeseries from some layers to work as percentile data for the
timeseries of another layer. Lizard-fancylayers can use that
information, and this functionality is used in the
grondwaterinbrabant-site.
