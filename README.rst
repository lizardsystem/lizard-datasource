lizard-datasource
==========================================

This is a library that defines a layer that goes between data sources
(of any kind, in principle), and the frontend of Lizard apps.

Data sources implement a subclass of
lizard_datasource.datasource.Datasource and a factory function that
returns instances of the subclass (one or many, up to the data
source). The factories are made available to lizard_datasource using
an entry point.

Lizard-Datasource then combines all the data sources it finds, and has
a function that returns a single Datasource instance. That single
instance represents all the data available in the system, and can be
used by apps to present all the data, or only the parts of it they
wish to show.

Lizard-Datasource also implements some data sources of its own;
notable the Dummy datasource that can be used for testing, and the
Augmented datasource which can take one or more data sources and
augment the data (color it, add percentiles, et cetera). Other
libraries could do the same thing.

See also lizard-fancylayers, a basic app for showing the datasource.
