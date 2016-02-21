from instagram.client import InstagramAPI


access_token = "243316452.1677ed0.aaf45b2c124449a3a53fc51ae5e0a214"
api = InstagramAPI(access_token=access_token,
			client_ips="8ab1830bac414c72b81daa905f890a3e",
			client_secret="b8608ed65a644382a82312113ac39af2")

media_with_location=[]
all_media_ids = []

media_ids,next = api.tag_recent_media(tag_name='france', count=1000)

position_tuple = ()

for media_id in media_ids:
	all_media_ids.append(media_id.id)
	#some media_ids don't have location assoicated with them... this maybe a hacky way of doing it, but it works
	if "location" in dir(media_id):
		#you can do it this way if that is the way you want your information, I did it using Tuples to have your data more organized and easir to access once its VERY large.
		#position = str(media_id.id) + "," + str(media_id.location.point.latitude) + ',' + str(media_id.location.point.longitude) + ';' + str(media_id.get_standard_resolution_url())

		# i found that some of the data doesn't have a full location ... so this just to check for that case.
		if ("point" in dir(media_id.location)) and ("latitude" in dir(media_id.location.point)) and ("longitude" in dir(media_id.location.point)):
			position_tuple=(str(media_id.id),str(media_id.location.point.latitude),str(media_id.location.point.longitude),str(media_id.get_standard_resolution_url()))
			media_with_location.append(position_tuple)

#print media_with_location

media_with_location2=[]
all_media_ids2 = []

media_ids2,next = api.tag_recent_media(tag_name='trip', count=1000)

position_tuple2 = ()

for media_id in media_ids2:
	all_media_ids2.append(media_id.id)
	#some media_ids don't have location assoicated with them... this maybe a hacky way of doing it, but it works
	if "location" in dir(media_id):
		#you can do it this way if that is the way you want your information, I did it using Tuples to have your data more organized and easir to access once its VERY large.
		#position = str(media_id.id) + "," + str(media_id.location.point.latitude) + ',' + str(media_id.location.point.longitude) + ';' + str(media_id.get_standard_resolution_url())

		# i found that some of the data doesn't have a full location ... so this just to check for that case.
		if ("point" in dir(media_id.location)) and ("latitude" in dir(media_id.location.point)) and ("longitude" in dir(media_id.location.point)):
			position_tuple2=(str(media_id.id),str(media_id.location.point.latitude),str(media_id.location.point.longitude),str(media_id.get_standard_resolution_url()))
			media_with_location2.append(position_tuple)

#print media_with_location2

trobat = None

for i in media_with_location:
	for j in media_with_location2:
		if (i==j and trobat==None):
			print i
			trobat = True

if (trobat == None):
	print media_with_location[0]

