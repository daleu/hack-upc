from TwitterSearch import *
try:
    predictions = ['golf course','parcel','land site']
    
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['flowering']) # let's define all words we would like to have a look for
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'VcVPqMF2AAe0u0V6YMq6sohDY',
        consumer_secret = 'vMHrqtTziJIRZLM57tpc57WzZXxll28HRXXoepFDQZmwf1fqFi',
        access_token = '2785738720-pyvnv3EJvkcn6W0q8G1G64Shdm2sKsOttFCicup',
        access_token_secret = 'bhm0XGbznwAmbWYwOlGnTfYTPi7fWaYpOOtXeZEMeEL6i'
     )

     # this is where the fun actually starts :)
    i = 0
    tso.set_keywords([predictions[i],'trip'])
    search = ts.search_tweets_iterable(tso)
    while i < len(predictions) and search.get_amount_of_tweets() == 0:
	++i
	tso.set_keywords([predictions[i]])
	search = ts.search_tweets_iterable(tso)
	
    for tweet in ts.search_tweets_iterable(tso):
	if tweet['coordinates']:
	    print( '@%s tweeted: %s \nurl: %s \ngeo: %s' % ( tweet['user']['screen_name'], tweet['text'], tweet['user']['url'], tweet['coordinates']['coordinates'] ) )

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)