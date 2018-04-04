
import datetime
import time

from gmaps import Geocoding
from TwitterSearch import (TwitterSearch, TwitterSearchException,
                           TwitterSearchOrder)


class TwSearchExperts():
    """
    Search and analysis of Twitter users who are experts in a specific domain
    """

    # class variables

    # list of types of keywords for searching experts in Twitter
    keywords_type_list = ['domain', 'expert']

    # list of categories of keywords for searching experts in Twitter
    keywords_category_list = ['tag', 'screen_name', 'hashtag', 'phrase']

    # class methods

    # ------------------------------------------------------
    def init_tw_search_lib(self, domain_keyword):
        """
        Init TwitterSearch Library 
        (Copyright (C) 2013 Christian Koepp
        https://github.com/ckoepp/TwitterSearch/tree/master)

        
        Arguments:
            domain_keyword {str} -- The keyword from <domain_keywords_dict> 
                                    that will be used to search in Twitter
        
        Returns:
            [TwitterSearch] -- TwitterSearch object with our secret tokens
            [TwitterSearchOrder] -- TwitterSearchOrder object with initialized attributes
        """

        try:
            tso = TwitterSearchOrder() # create a TwitterSearchOrder object
            tso.add_keyword(domain_keyword) # add keyword for search in Twitter
            tso.set_language('en') # we want to see English tweets only
            tso.set_include_entities(False) # and don't give us all those entity information

            # it's about time to create a TwitterSearch object with our secret tokens
            ts = TwitterSearch(
                consumer_key='<your-CONSUMER_KEY>',
                consumer_secret='<your-CONSUMER_SECRET>',
                access_token='<your-ACCESS_TOKEN>',
                access_token_secret='<your-ACCESS_TOKEN_SECRET>'
            )

        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)

        return ts, tso


    # -----------------------------------------------------------
    def create_domain_and_expert_keywords_dict(self,
                                               monexp_db,
                                               domain_json,
                                               keywords_category_list,
                                               flag_latin_chars):
        """
        Creates a following dictionaries:
        1. <domain_keywords_dict> -- Keywords with a score are used for a formal domain assessment
        2. <expert_keywords_dict> -- Keywords with a score are used for a formal experts assessment
        
        Arguments:
            monexp_db {MySQLMonExpDb} -- MySQLMonExpDb object (the MySQL database with domain expert data) 
            domain_json {dict} -- domain data in Python dictionary format
            keywords_category_list {list} -- ['tag', 'screen_name', 'hashtag', 'phrase']
            flag_latin_chars {bool} -- Indicates that the names of the members of the "tags" 
                                       and "expert_keywords" objects from the domains_data.json file 
                                       consist of only Latin characters. 
                                       Therefore, these lines can be used to search for Twitter 
                                       as a <screen_name>

        Returns:
            [int] -- <domain_id> from new inserted record in <keyword> DB table
            [dict] -- Created <domain_keywords_dict> from <domain_json> data
            [dict] -- Created <expert_keywords_dict> from <domain_json> data
        """

        domain_keywords_dict = dict()
        expert_keywords_dict = dict()

        domain = domain_json['domain']

        # insert <domain['domain']> data in <monexp_db>
        domain_id = monexp_db.insert_domain_in_db(domain)

        # Using "tags" array from <domain_json_data> for create <domain_keywords_dict>
        domain_json_tags_dict = domain_json['tags']

        #for tag_key, tag_score_value in domain_json_tags_dict.items():
        for tag in domain_json_tags_dict:
            keyword_type = 'domain'
            for keyword_category in keywords_category_list:
                if keyword_category == 'tag':
                    keyword = tag
                    keyword_score = domain_json_tags_dict[tag]
                    domain_keywords_dict[keyword] = keyword_score

                    # insert <keyword> in <keyword> DB table
                    keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_score, keyword_type, keyword_category,
                                                                domain_id)
                elif keyword_category == 'screen_name' and flag_latin_chars is True:
                    keyword = '@' + tag
                    keyword_score = domain_json_tags_dict[tag]
                    domain_keywords_dict[keyword] = keyword_score
                    
                    # insert <keyword> in <keyword> DB table
                    #keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_type, keyword_category, domain_id)
                    keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_score, keyword_type, keyword_category,
                                                                domain_id)
                elif keyword_category == 'hashtag':
                    keyword = '#' + tag
                    keyword_score = domain_json_tags_dict[tag]
                    domain_keywords_dict[keyword] = keyword_score

                    # insert <keyword> in <keyword> DB table
                    #keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_type, keyword_category, domain_id)
                    keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_score, keyword_type, keyword_category,
                                                                domain_id)

        # Using "phrases" array from <domain_json_data> for create <domain_keywords_list>
        domain_json_phrases_dict = domain_json['phrases']

        #for phrase_key, phrase_score_value in domain_json_phrases_dict.items():
        for phrase in domain_json_phrases_dict:
            keyword_type = 'domain'
            for keyword_category in keywords_category_list:
                if keyword_category == 'phrase':
                    keyword = phrase
                    keyword_score = domain_json_phrases_dict[phrase]
                    domain_keywords_dict[keyword] = keyword_score
                    
                    # insert <keyword> in <keyword> DB table
                    #keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_type, keyword_category, domain_id)
                    keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_score, keyword_type, keyword_category,
                                                                domain_id)

        # Using "expert_keywords" objects array from <domain_json_data> for create <expert_keywords_dict>
        # for expert in domain['experts']:
        domain_json_expert_dict = domain_json['expert_keywords']

        #for expert_key, expert_score_value in domain_json_expert_dict.items():
        for expert in domain_json_expert_dict:
            keyword_type = 'expert'
            for keyword_category in keywords_category_list:
                if keyword_category == 'tag':
                    keyword = expert
                    keyword_score = domain_json_expert_dict[expert]
                    expert_keywords_dict[keyword] = keyword_score

                    # insert <keyword> in <keyword> DB table
                    #keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_type, keyword_category, domain_id)
                    keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_score, keyword_type, keyword_category,
                                                                domain_id)
                elif keyword_category == 'screen_name' and flag_latin_chars is True:
                    keyword = '@' + expert
                    keyword_score = domain_json_expert_dict[expert]
                    expert_keywords_dict[keyword] = keyword_score

                    # insert <keyword> in <keyword> DB table
                    # keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_type, keyword_category, domain_id)
                    keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_score, keyword_type, keyword_category,
                                                                domain_id)
                elif keyword_category == 'hashtag':
                    keyword = '#' + expert
                    keyword_score = domain_json_expert_dict[expert]
                    expert_keywords_dict[keyword] = keyword_score

                    # insert <keyword> in <keyword> DB table
                    # keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_type, keyword_category, domain_id)
                    keyword_id = monexp_db.insert_keyword_in_db(keyword, keyword_score, keyword_type, keyword_category,
                                                                domain_id)

        return domain_id, domain_keywords_dict, expert_keywords_dict

    # ------------------------------------------------------------
    def analysis_tw_user_field(self,
                               tw_user_field_name,
                               tw_user_field_value,
                               domain_keywords_dict,
                               expert_keywords_dict,
                               analyze_expert_keyword_list_flag,
                               domain_analysis_tw_user_field_keywords_dict,
                               expert_analysis_tw_user_field_keywords_dict):
        """
        Analyze the specified following fields of the User object in Twitter:
            1. <screen_name>
            2. <name> AKA <user_name> in avtMonExp
            3. <description>
        
        Arguments:
            tw_user_field_name {str} -- Twitter user field name for analysis 
                                        ("screen_name", "name", or "description")
            tw_user_field_value {str} -- Value of the corresponding Twitter User field name
            domain_keywords_dict {dict} -- Keywords with a score are used for a formal domain assessment.
                                           Created from <domain_json> data
            expert_keywords_dict {dict} -- Keywords with a score are used for a formal experts assessment
                                           Created from <domain_json> data
            analyze_expert_keyword_list_flag {bool} -- Flag for analyzing the contents of the field 
                                                       to identify the Twitter user's belonging to experts 
                                                       in the given subject area
            domain_analysis_tw_user_field_keywords_dict {dict} -- Storage result of analysis 
                                                                  all domain keywords for 
                                                                  current found Twitter's user
            expert_analysis_tw_user_field_keywords_dict {dict} -- Storage result of analysis 
                                                                  all expert keywords for 
                                                                  current found Twitter's user
        """

        tw_user_field_value_lowercase = tw_user_field_value.lower()

        if tw_user_field_name == 'screen_name':
            for domain_keyword in domain_keywords_dict:
                if domain_keyword[0] == '@':
                    domain_keyword_lowercase = domain_keyword.lower()
                    domain_analysis_tw_user_field_keywords_dict[domain_keyword] = \
                        domain_analysis_tw_user_field_keywords_dict.get(domain_keyword, 0)
                    if tw_user_field_value_lowercase.find(domain_keyword_lowercase) != -1:
                        domain_analysis_tw_user_field_keywords_dict[domain_keyword] = \
                            domain_analysis_tw_user_field_keywords_dict.get(domain_keyword, 0) + 1

            if analyze_expert_keyword_list_flag is True:
                for expert_keyword in expert_keywords_dict:
                    if expert_keyword[0] == '@':
                        expert_keyword_lowercase = expert_keyword.lower()
                        expert_analysis_tw_user_field_keywords_dict[expert_keyword] = \
                            expert_analysis_tw_user_field_keywords_dict.get(expert_keyword, 0)
                        if tw_user_field_value_lowercase.find(expert_keyword_lowercase) != -1:
                            expert_analysis_tw_user_field_keywords_dict[expert_keyword] = \
                                expert_analysis_tw_user_field_keywords_dict.get(expert_keyword, 0) + 1

        elif tw_user_field_name == 'user_name':
            for domain_keyword in domain_keywords_dict:
                if domain_keyword[0] != '@' and \
                                domain_keyword[0] != '#' and \
                                domain_keyword.find(' ') == -1:
                    domain_keyword_lowercase = domain_keyword.lower()
                    domain_analysis_tw_user_field_keywords_dict[domain_keyword] = \
                        domain_analysis_tw_user_field_keywords_dict.get(domain_keyword, 0)
                    if tw_user_field_value_lowercase.find(domain_keyword_lowercase) != -1:
                        domain_analysis_tw_user_field_keywords_dict[domain_keyword] = \
                            domain_analysis_tw_user_field_keywords_dict.get(domain_keyword, 0) + 1

            if analyze_expert_keyword_list_flag is True:
                for expert_keyword in expert_keywords_dict:
                    if expert_keyword[0] != '@' and \
                                    expert_keyword[0] != '#' and \
                                    expert_keyword.find(' ') == -1:
                        expert_keyword_lowercase = expert_keyword.lower()
                        expert_analysis_tw_user_field_keywords_dict[expert_keyword] = \
                            expert_analysis_tw_user_field_keywords_dict.get(expert_keyword, 0)
                        if tw_user_field_value_lowercase.find(expert_keyword_lowercase) != -1:
                            expert_analysis_tw_user_field_keywords_dict[expert_keyword] = \
                                expert_analysis_tw_user_field_keywords_dict.get(expert_keyword, 0) + 1

        elif tw_user_field_name == 'description':
            for domain_keyword in domain_keywords_dict:
                domain_keyword_lowercase = domain_keyword.lower()
                domain_analysis_tw_user_field_keywords_dict[domain_keyword] = \
                    domain_analysis_tw_user_field_keywords_dict.get(domain_keyword, 0)
                if tw_user_field_value_lowercase.find(domain_keyword_lowercase) != -1:
                    domain_analysis_tw_user_field_keywords_dict[domain_keyword] = \
                        domain_analysis_tw_user_field_keywords_dict.get(domain_keyword, 0) + 1
            if analyze_expert_keyword_list_flag is True:
                for expert_keyword in expert_keywords_dict:
                    expert_keyword_lowercase = expert_keyword.lower()
                    expert_analysis_tw_user_field_keywords_dict[expert_keyword] = \
                        expert_analysis_tw_user_field_keywords_dict.get(expert_keyword, 0)
                    if tw_user_field_value_lowercase.find(expert_keyword_lowercase) != -1:
                        expert_analysis_tw_user_field_keywords_dict[expert_keyword] = \
                            expert_analysis_tw_user_field_keywords_dict.get(expert_keyword, 0) + 1
        else:
            print('Error message: Invalid field name for Twitter User object')



    # ----------------------------------------------------------------------------------------------
    def init_interval_scale(self, interval_scale_first_value, interval_scale_step, num_scores):
        """
        Init interval scale parameters
        
        Arguments:
            interval_scale_first_value {int} -- Initial value of the interval scale
            interval_scale_step {int} -- Interval scale step
            num_scores {int} -- Number of interval scale scores (marks, points, intervals)

        Returns:
            [list] -- Interval scale values
        """

        interval_scale_value_list = list()

        interval_scale_num_intervals = num_scores - 1
        interval_scale_value_i = interval_scale_first_value
        interval_scale_last_value = interval_scale_first_value + interval_scale_step * interval_scale_num_intervals

        while interval_scale_value_i <= interval_scale_last_value:
            interval_scale_value_list.append(interval_scale_value_i)
            interval_scale_value_i += interval_scale_step

        return interval_scale_value_list

    # ----------------------------------------------------------------------------------------------
    def calculating_tw_user_field_score (self, tw_user_field_value, interval_scale_value_list):
        
        """
        Calculates the score for the specified Twitter User field value
        
        Arguments:
            tw_user_field_value {int} -- Twitter User field value
            interval_scale_value_list {list} -- Interval scale values

        Returns:
            [int] -- Score for the specified Twitter User field value
        """

        interval_scale_first_value = interval_scale_value_list[0]
        interval_scale_last_value = interval_scale_value_list[len(interval_scale_value_list)-1]

        if tw_user_field_value < interval_scale_first_value:
            tw_user_field_score = 0
        elif tw_user_field_value >= interval_scale_last_value:
            tw_user_field_score = len(interval_scale_value_list)
        else:
            for i in range(len(interval_scale_value_list)-1):
                if (tw_user_field_value >= interval_scale_value_list[i]) and \
                        (tw_user_field_value < interval_scale_value_list[i+1]):
                    tw_user_field_score = i+1
                    break
        
        return tw_user_field_score

    # ----------------------------------------------------------------------------------------------
    def calculating_tw_user_keywords_score (self,
                                            keywords_dict,
                                            analysis_tw_user_field_keywords_dict):
        """
        Calculating the score for keywords that characterize a Twitter user. 
        From the point of view of an expert in this domain
        
        Arguments:
            keywords_dict {dict} -- <domain_keywords_dict> or 
                                    <expert_keywords_dict>
            analysis_tw_user_field_keywords_dict {dict} -- <domain_analysis_tw_user_field_keywords_dict> or
                                                           <expert_analysis_tw_user_field_keywords_dict>
        Returns:
            [int] -- Score for keywords that characterize a Twitter user.
        """

        # calculate <tw_user_keywords_score> as weighted average
        sum_weighted_average_numerator = 0
        # sum_weighted_average_denominator = sum(keywords_count_values_list)
        sum_weighted_average_denominator = 0

        for keyword in keywords_dict:
            sum_weighted_average_numerator += keywords_dict[keyword] * \
                                              analysis_tw_user_field_keywords_dict[keyword]
            sum_weighted_average_denominator += analysis_tw_user_field_keywords_dict[keyword]

        try:
            tw_user_keywords_score = round(sum_weighted_average_numerator / sum_weighted_average_denominator)
        except ZeroDivisionError:
            tw_user_keywords_score = 0

        return tw_user_keywords_score

    # --------------------------------------------------------------------------
    def analysis_tw_user_as_expert(self,
                                   tw_user_statuses_count,
                                   tw_user_followers_count,
                                   tw_user_friends_count,
                                   domain_keywords_dict,
                                   expert_keywords_dict,
                                   domain_analysis_tw_user_field_keywords_dict,
                                   expert_analysis_tw_user_field_keywords_dict):
        """
        Arguments:
            tw_user_statuses_count {int} -- The value of the <statuses_count> field of the User object in Twitter
            tw_user_followers_count {int} -- The value of the <followers_count> field of the User object in Twitter
            tw_user_friends_count {int} -- The value of the <friends_count> field of the User object in Twitter
            domain_keywords_dict {dict} -- Keywords with a score are used for a formal domain assessment.
                                           Created from <domain_json> data.
            expert_keywords_dict {dict} -- Keywords with a score are used for a formal experts assessment.
                                           Created from <domain_json> data.
            domain_analysis_tw_user_field_keywords_dict {dict} -- Storage result of analysis 
                                                                  all domain keywords for 
                                                                  current found Twitter's user
            expert_analysis_tw_user_field_keywords_dict {dict} -- Storage result of analysis 
                                                                  all expert keywords for 
                                                                  current found Twitter's user

        Returns:
            [bool] -- If the value of the <tw_user_is_expert> is True, 
                      then the current user of Twitter is an expert in this domain
            [int] -- tw_user_statuses_count_score
            [int] -- tw_user_followers_count_score
            [int] -- tw_user_friends_count_score
            [int] -- tw_user_domain_keywords_score
            [int] -- tw_user_expert_keywords_score
        """
        
        # init interval scale for calculating <tw_user_statuses_count_score> ,
        # <tw_user_followers_count_score> , <tw_user_friends_count_score>
        interval_scale_first_value = 500
        interval_scale_step = 100
        num_scores = 5
        interval_scale_value_list = self.init_interval_scale(interval_scale_first_value, interval_scale_step, num_scores)

        # calculating <tw_user_statuses_count_score> ,
        tw_user_statuses_count_score = self.calculating_tw_user_field_score(tw_user_statuses_count,
                                                                            interval_scale_value_list)
        # calculating <tw_user_followers_count_score> ,
        tw_user_followers_count_score = self.calculating_tw_user_field_score(tw_user_followers_count,
                                                                             interval_scale_value_list)

        # calculating <tw_user_followers_count_score> ,
        tw_user_friends_count_score = self.calculating_tw_user_field_score(tw_user_friends_count,
                                                                           interval_scale_value_list)

        # calculating <tw_user_domain_keywords_score>
        tw_user_domain_keywords_score = \
            self.calculating_tw_user_keywords_score(domain_keywords_dict,
                                                    domain_analysis_tw_user_field_keywords_dict)

        # calculating <tw_user_expert_keywords_score>
        tw_user_expert_keywords_score = \
            self.calculating_tw_user_keywords_score(expert_keywords_dict,
                                                    expert_analysis_tw_user_field_keywords_dict)

        # Checking the compliance of the current Twitter user with the expert's criteria
        # for the following calculated parameters (indicators):
        # 1. <tw_user_statuses_count_score>
        # 2. <tw_user_followers_count_score>
        # 3. <tw_user_friends_count_score>
        # 4. <tw_user_domain_keywords_score>
        # 5. <tw_user_expert_keywords_score>
        if (tw_user_statuses_count_score >= 1) and (tw_user_followers_count_score >= 1) and \
                (tw_user_friends_count_score >= 1) and (tw_user_domain_keywords_score >= 1) and \
                (tw_user_expert_keywords_score >= 1):
            tw_user_is_expert = True

        else:
            tw_user_is_expert = False

        return tw_user_is_expert, tw_user_statuses_count_score, tw_user_followers_count_score, \
            tw_user_friends_count_score, tw_user_domain_keywords_score, tw_user_expert_keywords_score
    
    # --------------------------------------------------------------------------
    def tw_expert_location_geocoding(self, tw_user_location):
        """
        Using data from the <tw_location> field in <monexp_db> database, 
        and python-gmaps Package as wrapper for Google Maps Geocoding API (as part of Google Maps API),
        get the latitude and longitude of the expert's location

        Arguments:
            tw_user_location {str} -- The value of the <tw_user_location> field 
                                      of the User object in Twitter
        
        Returns:
            [float] -- latitude of the expert's location or None, if the latitude was not determined
            [float] -- longitude of the expert's location or None, if the longitude was not determined
        """

        try:
            gmaps_request = Geocoding(api_key='<your-api_key>')
            gmaps_result = gmaps_request.geocode(tw_user_location)
            expert_location_lat = gmaps_result[0]['geometry']['location']['lat']
            expert_location_lng = gmaps_result[0]['geometry']['location']['lng']

        except:
            expert_location_lat = None
            expert_location_lng = None

        return expert_location_lat, expert_location_lng



    # --------------------------------------------------------------------------
    def tw_search_and_analysis_experts(self, all_domains_json, flag_latin_chars, monexp_db, avtmonexp_start_time):
        """
        Search experts in specified domain(s) from the Twitter users
        with TwitterSearch Library 
        (Copyright (C) 2013 Christian Koepp 
        https://github.com/ckoepp/TwitterSearch/tree/master)

        
        Arguments:
            all_domains_json {dict} -- domain data from "domains_data.json" file
            flag_latin_chars {bool} -- Indicates that the names of the members of the "tags" 
                                       and "expert_keywords" objects from the domains_data.json file
                                       consist of only Latin characters.
                                       Therefore, these lines can be used to search for Twitter
                                       as a <screen_name>
            monexp_db {MySQLMonExpDb} -- MySQLMonExpDb object 
                                         (the MySQL database with domain expert data)
            avtmonexp_start_time {float} -- avtMonExp start time
        """


        # -------------------------------------------------------------
        # 1) Prepare following data for Search with TwitterSearch Lib
        #    and analysis results to be found
        #    1.1) Creating a <domain_keywords_list> to identify domain
        #    1.2) Creating a <expert_keywords_list> to identify experts
        #         in the processing domain (subject area)
        # -------------------------------------------------------------

        monexp_db.create_keywords_reference_db_tables(self.keywords_type_list, self.keywords_category_list)

        # Start processing <domain_data_json> for add values
        # to <domain_keywords_list> and <expert_keywords_list>
        for domain_json in all_domains_json['domains']:
            
            print('\n ---')
            print(' Current processing domain: ', domain_json['domain'])

            # Create dictionaries(service dictionaries) for domain search keywords (<domain_keywords_dict>) and
            # experts search keywords (<expert_keywords_dict>)
            domain_id, domain_keywords_dict, expert_keywords_dict = \
                self.create_domain_and_expert_keywords_dict(monexp_db,
                                                            domain_json,
                                                            self.keywords_category_list,
                                                            flag_latin_chars)

            # -------------------------------------------------------------------------------------
            # 2) Start Search with TwitterSearch Library on base created <domain_keywords_dict>
            #    and analysis found results with <domain_keywords_dict> and <expert_keywords_dict>
            # -------------------------------------------------------------------------------------

            for domain_keyword in domain_keywords_dict:

                ts, tso = self.init_tw_search_lib(domain_keyword)

                # avoid rate-limitation using a callback method
                def my_callback_closure(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
                    queries, tweets_seen = current_ts_instance.get_statistics()
                    print('\n Queries done: %i. Tweets received: %i' % (queries, tweets_seen))
                    # trigger delay every 5th query
                    if queries > 0 and (queries % 5) == 0: 
                        
                        # avtMonExp current run time
                        avtmonexp_current_time = time.time()

                        # The avtMonExp run elapsed time
                        avtmonexp_run_elapsed_time = avtmonexp_current_time - avtmonexp_start_time 
                        
                        print('\n ---')
                        print(' Current time(UTC): ', time.strftime("%H:%M:%S", time.gmtime(avtmonexp_current_time)))
                        print(' Elapsed time: ', time.strftime("%H:%M:%S", time.gmtime(avtmonexp_run_elapsed_time)))
                        
                        print('\n ---')
                        print(' Now the avtMonExp app is suspended for 60 seconds to avoid rate-limitation by Twitter...')
                        time.sleep(60) # sleep for 60 seconds
                        
                        print('\n ---')
                        print(' Resume processing and analysis...')

                for tw_user in ts.search_tweets_iterable(tso, callback=my_callback_closure):

                    # Twitter user id_str
                    tw_user_id_str = tw_user['user']['id_str']

                    # Checking the presence of the <tw_user> in the <tw_expert> DB table
                    tw_expert_id = monexp_db.find_tw_expert_in_db(tw_user_id_str)

                    # If <tw_user_id_str> not found in <tw_expert> DB table (tw_expert_id == -1),
                    # then start(begin) deep analysis current found Twitter user with TwitterSearch Library
                    # as expert in corrent domain.
                    # If the analysis of the current Twitter user reveals an expert,
                    # then we add this Twitter's user to the <tw_expert> DB table in <monexp_db> database as an expert
                    # In the opposite case, go to the next user of Twitter
                    # (update(delete) expert record from DB + start new analysis as expert + insert) Twitter expert data)
                    if tw_expert_id == -1:

                        # Create new empty dictionaries for storage result of analysis all domain and expert keywords
                        # for current found Twitter's user
                        domain_analysis_tw_user_field_keywords_dict = dict()
                        expert_analysis_tw_user_field_keywords_dict = dict()

                        # Twitter user <screen_name> (The field to be analyzed!)
                        tw_user_screen_name = tw_user['user']['screen_name']
                        tw_user_screen_name = tw_user_screen_name.strip().lower()
                        if flag_latin_chars is True:
                                self.analysis_tw_user_field('screen_name', tw_user_screen_name,
                                                            domain_keywords_dict,
                                                            expert_keywords_dict,
                                                            False,
                                                            domain_analysis_tw_user_field_keywords_dict,
                                                            expert_analysis_tw_user_field_keywords_dict)

                        # Twitter user <name> (The field to be analyzed!)
                        tw_user_name = tw_user['user']['name']
                        tw_user_name = tw_user_name.lower()
                        self.analysis_tw_user_field('user_name', tw_user_screen_name,
                                                    domain_keywords_dict,
                                                    expert_keywords_dict,
                                                    True,
                                                    domain_analysis_tw_user_field_keywords_dict,
                                                    expert_analysis_tw_user_field_keywords_dict)

                        # Twitter user <description> (The field to be analyzed!)
                        tw_user_description = tw_user['user']['description']
                        tw_user_description = tw_user_description.lower()
                        self.analysis_tw_user_field('description', tw_user_description,
                                                    domain_keywords_dict,
                                                    expert_keywords_dict,
                                                    True,
                                                    domain_analysis_tw_user_field_keywords_dict,
                                                    expert_analysis_tw_user_field_keywords_dict)

                        # Twitter user <statuses_count> (The field to be analyzed!)
                        tw_user_statuses_count = tw_user['user']['statuses_count']

                        # Twitter user <followers_count> (The field to be analyzed!)
                        tw_user_followers_count = tw_user['user']['followers_count']

                        # Twitter user <friends_count> (The field to be analyzed!)
                        tw_user_friends_count = tw_user['user']['friends_count']

                        # Twitter user <location>
                        tw_user_location = tw_user['user']['location']

                        # Twitter user <lang>
                        tw_user_lang = tw_user['user']['lang']

                        # Analysis of the current Twitter user as an expert
                        tw_user_is_expert, tw_user_statuses_count_score, tw_user_followers_count_score, \
                            tw_user_friends_count_score, tw_user_domain_keywords_score, \
                            tw_user_expert_keywords_score = \
                            self.analysis_tw_user_as_expert(tw_user_statuses_count,
                                                            tw_user_followers_count,
                                                            tw_user_friends_count,
                                                            domain_keywords_dict,
                                                            expert_keywords_dict,
                                                            domain_analysis_tw_user_field_keywords_dict,
                                                            expert_analysis_tw_user_field_keywords_dict)

                        if tw_user_is_expert is True:

                            # Search latitude and longitude for found expert by <tw_location> field 
                            # in <monexp_db> with python-gmaps Package as wrapper for 
                            # Google Maps Geocoding API (as part of Google Maps API) 
                            expert_location_lat, expert_location_lng = \
                                self.tw_expert_location_geocoding(tw_user_location)

                            # Insert current <tw_user> data in the <tw_expert> DB table
                            tw_expert_id = monexp_db.insert_tw_expert_in_db(tw_user_id_str,
                                                                            tw_user_screen_name,
                                                                            tw_user_name,
                                                                            tw_user_description,
                                                                            tw_user_statuses_count,
                                                                            tw_user_statuses_count_score,
                                                                            tw_user_followers_count,
                                                                            tw_user_followers_count_score,
                                                                            tw_user_friends_count,
                                                                            tw_user_friends_count_score,
                                                                            tw_user_location,
                                                                            expert_location_lat,
                                                                            expert_location_lng,
                                                                            tw_user_lang,
                                                                            tw_user_domain_keywords_score,
                                                                            tw_user_expert_keywords_score,
                                                                            domain_id)

                            # Insert keywords that evaluate the current expert <tw_expert_id> in the
                            # <tw_expert_keywords> DB table
                            monexp_db.insert_tw_expert_keywords_in_db(tw_expert_id,
                                                                      domain_id,
                                                                      domain_analysis_tw_user_field_keywords_dict,
                                                                      expert_analysis_tw_user_field_keywords_dict)
