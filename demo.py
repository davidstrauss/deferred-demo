from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor, utils
from twisted.python import log
import sys
import pprint

class DeferredDemo(Resource):
  def __init__(self):
      Resource.__init__(self)

  def render_GET(self, request):
      response = utils.getProcessOutputAndValue("/usr/bin/time", args=["/bin/sleep", "3"])
      def cbBody(results):
          pprint.pprint(results)
          (_, text, _) = results
          body = str(len(text))
          request.write(body)
          request.finish()
      result = response.addCallback(cbBody)
      return NOT_DONE_YET

  def getChild(self, name, request):
      return self

log.startLogging(sys.stdout)
root = DeferredDemo()
factory = Site(root)
reactor.listenTCP(9090, factory)
reactor.run()
