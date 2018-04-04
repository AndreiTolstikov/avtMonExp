
import os
import shutil
import subprocess
import sys

import gmplot


class ExpertsDataViz():
    """
    Generate the HTML and javascript 
    to render geographical coordinates of experts on top of Google Maps
    """


    def generate_html_view_tw_experts_from_domain_on_gmap(self, monexp_db, domain, generated_html_gmap_file_name):
        """
        Plotting expert data from the specified domain on Google Maps.
        A matplotlib-like interface to generate the HTML and javascript
        to render all the data you'd like on top of Google Maps.
        Several plotting methods make creating exploratory map views effortless.
        
        Arguments:
            monexp_db {MySQLMonExpDb} -- expert data from monexp_db database
            domain {string} -- name of domain(subject area) for expert search
            generated_html_gmap_file_name {string} -- the HTML file name (with javascript)
                                                      to render geographical coordinates
                                                      of experts on top of Google Maps
        """

        # Find all records with <expert_location_lat> and <expert_location_lng>,
        # which are not NULL in <tw_expert> DB table (expert data)
        expert_domain_t, expert_location_lat_lng_t = monexp_db.find_tw_expert_location_lat_lng_in_db(domain)

        # If specified <domain> not found in <domain> DB table
        if expert_domain_t is None:
            print('\n ---')
            print(' <domain> = %s not found in <monexp_db>.' % (domain))
            print(' HTML-file %s note generated' % (generated_html_gmap_file_name))

        # If <expert_location_lat> and <expert_location_lng>,
        # which are not NULL not found in <tw_expert> DB table (expert data)
        elif expert_location_lat_lng_t is None:
            print('\n ---')
            print(' <expert_location> coordinates(lat,lng) not found in <monexp_db>.')
            print(' HTML-file %s note generated' % (generated_html_gmap_file_name))

        # generate the HTML and javascript to render <expert_location_lat>
        # and <expert_location_lng> data on top of Google Maps
        else:

            # some code for generate HTML
            gmap = gmplot.GoogleMapPlotter(42.458049, 3.339844, 5)

            # prepare <expert_location_lats_list> and <expert_location_lngs_list>
            expert_location_lats_list = list()
            expert_location_lngs_list = list()

            for i in range(len(expert_location_lat_lng_t)):
                expert_location_lats_list.append(expert_location_lat_lng_t[i][0])
                expert_location_lngs_list.append(expert_location_lat_lng_t[i][1])

            # prepare tw_expert coordinates 
            # (<expert_location_lats_list> and <expert_location_lngs_list>)
            # for plotting on Google Map
            gmap.heatmap(expert_location_lats_list, expert_location_lngs_list)
            
            # The directory that contains the executable file of the project(avtmonexp.py)
            # will be made current
            # os.chdir(os.path.dirname(os.path.abspath(generated_html_gmap_file_name)))
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
            # Get absolute path to <generated_html_gmap_file_name>
            generated_html_gmap_full_file_name = \
                os.path.abspath(r'experts_data_viz_html/'+generated_html_gmap_file_name)

            # The project directory <experts_data_viz_html> that contains the generated html files
            # will be made current
            os.chdir(os.path.dirname(generated_html_gmap_full_file_name))

            # If <generated_html_gmap_full_file_name> already exists
            # then chenge it extensions from *.html to *.bak
            if os.path.exists(generated_html_gmap_full_file_name):
                try:
                    backup_html_gmap_file_name = generated_html_gmap_file_name[:-4]+'bak'
                    #backup_html_gmap_full_file_name=os.path.abspath(backup_html_gmap_file_name)
                    #if os.path.exists(backup_html_gmap_full_file_name):
                    #os.rename(generated_html_gmap_file_name, backup_html_gmap_file_name)
                    shutil.copy(generated_html_gmap_file_name, backup_html_gmap_file_name)
                    print('\n ---')
                    print(' Copy exists <%s> file to <%s> file...' \
                         % (generated_html_gmap_file_name, backup_html_gmap_file_name))
                except OSError:
                    print('\n The <%s> file could not be copy to <%s> file' \
                         % (generated_html_gmap_file_name, backup_html_gmap_file_name))
            
            # generate 'experts_on_gmap_domain_name.html'file and save into 
            # 'experts_data_viz_html/' project folder
            gmap.draw(generated_html_gmap_file_name)
            print('\n ---')
            print(' New <%s> file was successfully generated...' % (generated_html_gmap_file_name))
            
            # Open generated HTML file in default browser
            print('\n ---')
            print(' Open new <%s> file in default browser...' % (generated_html_gmap_file_name))
            subprocess.Popen(['start', generated_html_gmap_file_name], shell=True)
