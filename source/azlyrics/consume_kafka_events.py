import datetime
import json
import download_songs, download_lyrics
from source.azlyrics import argparse_utils
from kafka import KafkaConsumer


def consume_events(metadb, topic, server, group_id=None):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=server,
        group_id=group_id,
        auto_offset_reset="latest",
        value_deserializer=lambda value: json.loads(value.decode("utf-8"))
        # add more configs here if you'd like
    )

    # message_format: {"title":string,"url":string,"artist":string,"slug":string,"status":boolean}
    try:
        for msg in consumer:
            # get the JSON deserialized value
            value = msg.value
            
            artist = value["artist"]
            title = value["title"]
            url = value["url"]
            slug = value["slug"]
            status = value["status"] if "status" in value else False
            
            download_songs.DB.insert_songs_into_db(metadb, artist=artist, 
                                                   songs=(title, url),
                                                   slug=slug)
            
            print(f"Successfully processed song by artist: '{artist}' titled: '{title}'")
            
            if status:
                download_lyrics.update_songs_db(metadb, artist=artist, song=slug)
                print(f"lyrics downloaded.")

            
            
    except:
        print("Could not consume from topic: {self.topic}")
        raise

if __name__ == '__main__':
        
    parser = argparse_utils.parser
    
    parser.add_argument(
        '--topic',
        type=str,
        required=True,
        help='Kafka topic')
    
    parser.add_argument(
        '--server',
        type=str,
        required=True,
        help='Kafka server')
    
    parser.add_argument(
        '--group',
        type=str,
        required=False,
        help='Kafka consumer group')
    
    args = parser.parse_args()
    
    if not args.metadatadb:
        raise Exception("Metadata db not provided")
    
    consume_events(args.metadatadb, args.topic, args.server, args.group)