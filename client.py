import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType

filter1 = Filter(
                    authors=["ca0b427245702954452d3876f01081e9b191f4130bbe9530c5278d9f8fd2600f"], 
                    kinds=[1]
                )
# my_tags =init_filter.add_arbitrary_tag("t",["hashtag","developing"])
filter1.add_arbitrary_tag("t",["hashtag","developing","zap"])
filters = Filters([filter1])

subscription_id = "hello"
request = [ClientMessageType.REQUEST, subscription_id]
request.extend(filters.to_json_array())

relay_manager = RelayManager()
relay_manager.add_relay("wss://puravida.nostr.land")
relay_manager.add_relay("wss://nostr.wine")
relay_manager.add_subscription(subscription_id, filters)
relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(1.25) # allow the connections to open

message = json.dumps(request)
relay_manager.publish_message(message)
time.sleep(1) # allow the messages to send

while relay_manager.message_pool.has_events():
  event_msg = relay_manager.message_pool.get_event()
  print('--->>>')
  print('id: '+event_msg.event.id)
  print('pubkey: '+event_msg.event.public_key)
  print('created_at: '+str(event_msg.event.created_at))
  print('kind: '+str(event_msg.event.kind))
  print('tags: '+ str(event_msg.event.tags))
  print('content: '+event_msg.event.content)
  print('sig: '+event_msg.event.signature)
  print('url: '+event_msg.url)
  print('<<<---')
  
relay_manager.close_connections()