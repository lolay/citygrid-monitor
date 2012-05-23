import logging
import webapp2
import urllib2
import json
import uuid

publisher = "4214549098"
placement = "monitor"

class CityGridHandler(webapp2.RequestHandler):
	def get_search_location(self, what, where, listing_id,):
		logger = logging.getLogger("citygrid.CityGridHandler.get_search_location")
		logger.debug("ENTER what=%(what)s, where=%(where)s, listing_id=%(listing_id)s", {"what": what, "where": where, "listing_id": listing_id})

		url = "http://api.citygridmedia.com/content/places/v2/search/where?what=%(what)s&client_ip=%(remote_address)s&where=%(where)s&publisher=%(publisher)s&placement=%(placement)s&format=json" %\
			  {"what": urllib2.quote(what), "where": urllib2.quote(where), "publisher": publisher, "placement": placement, "remote_address": self.request.remote_addr}
		logger.debug("url=%(url)s", {"url": url})

		fp = urllib2.urlopen(url)
		parsed = json.load(fp)

		logger.debug("parsed=%(parsed)s", {"parsed": parsed})

		location = None
		for location in parsed["results"]["locations"]:
			logger.debug("location id=%(id)s, name=%(name)s", {"id": location["id"], "name": location["name"]})
			if listing_id == location["id"]:
				location = location
				break
		return location

	def get_detail_location(self, search_location):
		logger = logging.getLogger("citygrid.CityGridHandler.get_detail_location")
		logger.debug("ENTER search_location=%(search_location)s", {"search_location": search_location})

		if search_location == None:
			return None

		listing_id = search_location["id"]
		impression_id = search_location["impression_id"]

		url = "http://api.citygridmedia.com/content/places/v2/detail?client_ip=%(remote_address)s&placement=%(placement)s&all_results=false&publisher=%(publisher)s&i=%(impression_id)s&listing_id=%(listing_id)s&format=json" %\
			  {"remote_address": self.request.remote_addr, "placement": placement, "publisher": publisher, "impression_id": impression_id, "listing_id": listing_id}
		logger.debug("url=%(url)s", {"url": url})

		fp = urllib2.urlopen(url)
		parsed = json.load(fp)

		logger.debug("parsed=%(parsed)s", {"parsed": parsed})

		location = parsed["locations"][0]
		return location

	def track_location(self, detail_location, action_target):
		logger = logging.getLogger("citygrid.CityGridHandler.track_location")
		logger.debug("ENTER detail_location=%(detail_location)s, action_target=%(action_target)s", {"detail_location": detail_location, "action_target": action_target})

		if detail_location == None:
			return False

		listing_id = detail_location["id"]
		impression_id = detail_location["impression_id"]
		reference_id = detail_location["reference_id"]
		device_id = str(uuid.uuid4())

		url = "http://api.citygridmedia.com/ads/tracker/imp?reference_id=%(reference_id)s&placement=%(placement)s&mobile_type=iPhone%%20Monitor&muid=%(device_id)s&publisher=%(publisher)s&i=%(impression_id)s&listing_id=%(listing_id)s&action_target=%(action_target)s" %\
			  {"reference_id": reference_id, "placement": placement, "device_id": device_id, "publisher": publisher, "impression_id": impression_id, "listing_id": listing_id, "action_target": action_target}
		logger.debug("url=%(url)s", {"url": url})

		data = urllib2.urlopen(url).read()
		if data != None:
			return True
		else:
			return False

	def get(self):
		logger = logging.getLogger("citygrid.CityGridHandler.get")
		logger.debug("ENTER")

		what=self.request.get("what")
		where=self.request.get("where")
		listing_id=int(self.request.get("listing_id"))

		search_location = self.get_search_location(what, where, listing_id)
		if search_location != None:
			logger.debug("search_location=%(search_location)s", {"search_location": search_location})
		else:
			self.response.out.write("Search Location %(listing_id)s not found" % {"listing_id": listing_id})
			return

		detail_location = self.get_detail_location(search_location)
		if detail_location != None:
			logger.debug("detail_location=%(detail_location)s", {"detail_location": detail_location})
		else:
			self.response.out.write("Detail Location %(search_location)s not found" % {"search_location": search_location})
			return

		tracked_profile = self.track_location(detail_location, "listing_profile")
		if tracked_profile:
			logger.debug("profile tracked")
		else:
			self.response.out.write("Profile tracking failed for %(detail_location)s not found" % {"detail_location": detail_location})
			return

		tracked_review = self.track_location(detail_location, "listing_review")
		if tracked_review:
			logger.debug("review tracked")
		else:
			self.response.out.write("Review tracking failed for %(detail_location)s not found" % {"detail_location": detail_location})
			return

		tracked_map = self.track_location(detail_location, "listing_map")
		if tracked_map:
			logger.debug("map tracked")
		else:
			self.response.out.write("Map tracking failed for %(detail_location)s not found" % {"detail_location": detail_location})
			return

		self.response.out.write("Success")
