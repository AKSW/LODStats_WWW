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
    rdfstats_runner = rdfstats.commands.rdfstats_runner:DoStats
    rdfstats_custom_runner = rdfstats.commands.rdfstats_custom_runner:DoStats
    rdf_ckan_update = rdfstats.commands.rdf_ckan_update:DoUpdate
    admin = rdfstats.commands.admin:DoAdmin
    clean_workers = rdfstats.commands.clean_workers:DoCleanWorkers
    clean_workers_custom = rdfstats.commands.clean_workers_custom:DoCleanWorkers
    load_from_pickled = rdfstats.commands.load_from_pickled:DoLoadFromPickled
    db_manipulation = rdfstats.commands.db_manipulation:DoDB
    update_from_file = rdfstats.commands.update_from_file:UpdateFromFile
    process_all_datasets = rdfstats.commands.process_all_datasets:ProcessAllDatasets
    lodstats_listener = rdfstats.commands.lodstats_listener:LodstatsListener
    """,
)
