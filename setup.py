try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='rdfstats',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "Pylons>=1.0",
        "SQLAlchemy>=0.6.4",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'rdfstats': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'rdfstats': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = rdfstats.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [paste.paster_command]
    process_all_datasets = rdfstats.commands.process_all_datasets:ProcessAllDatasets
    process_by_id = rdfstats.commands.process_by_id:ProcessById
    lodstats_listener = rdfstats.commands.lodstats_listener:LodstatsListener
    debug = rdfstats.commands.debugger:Debugger
    lodstats_update = rdfstats.commands.lodstats_update:LodstatsUpdate
    lodstats_sync = rdfstats.commands.synchronize_ckan:SynchronizeCkan
    """,
)
