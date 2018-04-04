
import datetime
import time

import experts_data_viz
import mysql_monexp_db
import prepare_domains_data
import tw_search_experts


print('\n ------------------------------------------------------------------')
print(' The avtMonExp app began to search and analyze experts on Twitter ...')
print(' --------------------------------------------------------------------')

# avtMonExp start time
avtmonexp_start_time = time.time()

print('\n ---')
print(' Timestamp (UTC): ', time.strftime("%Y-%b-%d %H:%M:%S", time.gmtime(avtmonexp_start_time)))

# Prepare domains data from JSON file (by default "domains_data.json") for further processing
domains_data_file_name = r'domains_data.json'
print('\n ---')
print(' Prepare data from <%s> file...' % domains_data_file_name)

all_domains_json = prepare_domains_data.load_domains_data(domains_data_file_name)

# Prepare to work with monexp_db (as MySQL)

# Create MySQLMonExpDb() class instance
monexp_db = mysql_monexp_db.MySQLMonExpDb()

# Create monexp_db
print('\n ---')
print(' Create <monexp_db> database...')
monexp_db.create_db()

# Create DB tables in monexp_db
print('\n ---')
print(' Create tables in <monexp_db> database...')
monexp_db.create_db_tables()

# Create TwSearchExperts() class instance
ts_experts = tw_search_experts.TwSearchExperts()

# Search domain experts from Twitter users
print('\n ---')
print(' Search and analysis experts from Twitter users...')
ts_experts.tw_search_and_analysis_experts(all_domains_json, True, 
                                            monexp_db, avtmonexp_start_time)

# Create ExpertsDataViz() class instance
experts_data_viz_on_gmap = experts_data_viz.ExpertsDataViz()

# Display experts for each domain on Google Maps
print('\n ---')
print(' Generate HTML and display experts for each domain on Google Maps in default browser...')
for domain_json in all_domains_json['domains']:
    domain = domain_json['domain']
    generate_html_filename = domain + '_experts' + '.html'
    experts_data_viz_on_gmap.generate_html_view_tw_experts_from_domain_on_gmap(monexp_db, domain, generate_html_filename)

# avtMonExp end time
avtmonexp_end_time = time.time()

# The avtMonExp run elapsed time
avtmonexp_run_elapsed_time = avtmonexp_end_time - avtmonexp_start_time 

print('\n ---')
print(' Timestamp (UTC): ', time.strftime("%Y-%b-%d %H:%M:%S", time.gmtime(avtmonexp_end_time)))

print('\n ---------------------------------------------------------------------')
print(' The avtMonExp app successfully completed.')
print(' -----------------------------------------------------------------------')
print(' Elapsed time: ', time.strftime("%H:%M:%S", time.gmtime(avtmonexp_run_elapsed_time)))
print(' -----------------------------------------------------------------------')
