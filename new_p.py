import time
import logging
import argparse
import datetime
import json
from google.cloud import pubsub
from sodapy import Socrata
def get_timestamp(line):
   # look at first field of row
   timestamp = line.split(',')[0]
   return datetime.datetime.strptime(timestamp, TIME_FORMAT)
def peek_timestamp(ifp):
   # peek ahead to next line, get timestamp and go back
   pos = ifp.tell()
   line = ifp.readline()
   ifp.seek(pos)
   return get_timestamp(line)
def api_invoke():
# Example authenticated client (needed for non-public datasets):
    client = Socrata("data.cityofchicago.org", None)
    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("8v9j-bter", content_type="json", limit=20)
    return results
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Send sensor data to Cloud Pub/Sub')
   parser.add_argument('--project', help='Example: --project $DEVSHELL_PROJECT_ID', required=True)
   args = parser.parse_args()
   # create Pub/Sub notification topic
   logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
   publisher = pubsub.PublisherClient()
   topic_path = publisher.topic_path(args.project,'chicago')
   #topic_path = publisher.topic_path('superb-celerity-203613', 'chicago')
   #try:
    #  publisher.get_topic(event_type)
     # logging.info('Reusing pub/sub topic {}'.format(TOPIC))
   #except:
    #  publisher.create_topic(event_type)
     # logging.info('Creating pub/sub topic {}'.format(TOPIC))
   # notify about each line in the input file
   programStartTime = datetime.datetime.utcnow()
   data = api_invoke()
   json_str = json.dumps(data)
   publisher.publish(topic_path,json_str)
   #print(data[1])
   #for event_data in json_str:
    #    publisher.publish(topic_path, event_data)
