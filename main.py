import logging
import webapp2
from citygrid import CityGridHandler

# GAE creates a root logger already, so have to set the formatter
logging.getLogger().handlers[0].setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s  %(module)s.%(funcName)s:%(lineno)d %(message)s"))

app = webapp2.WSGIApplication([('/citygrid', CityGridHandler)], debug=True)
