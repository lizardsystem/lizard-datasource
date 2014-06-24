import logging

from celery.task import task

from lizard_datasource import datasource
from lizard_datasource import scripts
from lizard_ui.multitenancy import set_host


logger = logging.getLogger(__name__)


@task
def cache_latest_values(*args, **options):
    """Celery task for cache_latest_values.

    Original from the cache_latest_values management command."""

    # Set host for lizard 5 multitenancy.
    if 'host' in options:
        set_host(options['host'])

    for ds in datasource.datasources_from_entrypoints():
        try:
            scripts.cache_latest_values(ds)
        except:
            logger.exception('skipping datasource {0}'.format(ds))
