import logging
import webapp2
import urllib2
import json

publisher = "4214549098"
placement = "monitor"

class CityGridHandler(webapp2.RequestHandler):
	def get(self):
		logger = logging.getLogger("citygrid.CityGridHandler.get")
		logger.debug("ENTER")

		what=self.request.get("what")
		where=self.request.get("where")
		listing_id=int(self.request.get("listing_id"))

		logger.debug("what=%(what)s, where=%(where)s, listing_id=%(listing_id)s", {"what": what, "where": where, "listing_id": listing_id})

		cg_search_url = "http://api.citygridmedia.com/content/places/v2/search/where?what=%(what)s&client_ip=%(remote_address)s&where=%(where)s&publisher=%(publisher)s&placement=%(placement)s&format=json" % {"what": urllib2.quote(what), "where": urllib2.quote(where), "publisher": publisher, "placement": placement, "remote_address": self.request.remote_addr}
		logger.debug("cg_search_url=%(cg_search_url)s" % {"cg_search_url": cg_search_url})

		cg_search_fp = urllib2.urlopen(cg_search_url)
		cg_search_parsed = json.load(cg_search_fp)

		logger.debug("cg_search_parsed=%(cg_search_parsed)s", {"cg_search_parsed": cg_search_parsed})

		cg_search_location = None
		for location in cg_search_parsed["results"]["locations"]:
			logger.debug("location id=%(id)s, name=%(name)s", {"id": location["id"], "name": location["name"]})
			if listing_id == location["id"]:
				cg_search_location = location
				break

		if cg_search_location != None:
			logger.debug("cg_search_location=%(cg_search_location)s", {"cg_search_location": cg_search_location})
		else:
			self.response.out.write("Location %(listing_id)s not found" % {"listing_id": listing_id})
			return

#http://api.citygridmedia.com/content/places/v2/detail?client_ip=127.0.0.1&customer_only=false&placement=demo-sdk&format=json&all_results=false&publisher=4214549098&i=000b0000001b45849161d94dd5b9dfb07d727bc84e&listing_id=603514592
#http://api.citygridmedia.com/ads/tracker/imp?reference_id=1&dialPhone=3102782050&placement=demo-sdk&mobile_type=iPhone%20Simulator&muid=B4B53725-EBAC-5A7A-9BB9-9B6BEADB023C&format=json&publisher=4214549098&i=0009000000212f149d8d164873bd8d56340495abcc&listing_id=603514592&action_target=listing_profile
#http://api.citygridmedia.com/ads/tracker/imp?reference_id=1&dialPhone=3102782050&placement=demo-sdk&mobile_type=iPhone%20Simulator&muid=B4B53725-EBAC-5A7A-9BB9-9B6BEADB023C&format=json&publisher=4214549098&i=0009000000212f149d8d164873bd8d56340495abcc&listing_id=603514592&action_target=listing_review
#http://api.citygridmedia.com/ads/tracker/imp?reference_id=1&dialPhone=3102782050&placement=demo-sdk&mobile_type=iPhone%20Simulator&muid=B4B53725-EBAC-5A7A-9BB9-9B6BEADB023C&format=json&publisher=4214549098&i=0009000000212f149d8d164873bd8d56340495abcc&listing_id=603514592&action_target=listing_map

		self.response.out.write("Success")
