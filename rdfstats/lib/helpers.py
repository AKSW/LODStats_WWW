"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html.tags import link_to
from webhelpers.html.tags import form, end_form, submit, stylesheet_link, javascript_link, th_sortable
from webhelpers.date import distance_of_time_in_words
from webhelpers.text import plural
from webhelpers.number import format_data_size
from webhelpers.number import percent_of
from webhelpers.number import format_number
from webhelpers.text import truncate
