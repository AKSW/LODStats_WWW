#sparqlify -h localhost -U postgres -W postgres -d lodstats -m ./mappings/rdfdoc.sml -D > ./datasets/rdfdoc.nt
#sparqlify -h localhost -U postgres -W postgres -d lodstats -m ./mappings/ckan_catalog.sml -D > ./datasets/ckan_catalog.nt
sparqlify -h localhost -U postgres -W postgres -d lodstats -m ./mappings/stat_result.sml -D > ./datasets/stat_result.nt
