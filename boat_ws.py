import websocket

WS_SERVER = "192.168.0.21"
WS_PORT = "13000"

def JSONify(confidence, heading):
  my_string = '{"vision_data":'
  my_string += '{ "heading":%s,' % str(heading)
  my_string += '"confidence":%s}}' % str(confidence)
  return my_string

