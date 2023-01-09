from kafka.admin import KafkaAdminClient, NewTopic, ConfigResource, ConfigResourceType
import kafka
import boto3
import os
import json


def lambda_handler(event, context):
    try:
        whichfunction =  event["queryStringParameters"]["whichfunction"]
        bsrv =  event["queryStringParameters"]["bsrv"]
        a=""
        if whichfunction=='listtopics':
            a=getTopicList(bsrv)
        elif whichfunction=='gettopicconfig':
            topicname=event["queryStringParameters"]["topicname"]
            a=getTopicConfig(topicname,bsrv)
        elif whichfunction=='createtopic':
            topicname=event["queryStringParameters"]["topicname"]
            retention=event["queryStringParameters"]["retention"]
            localretention=event["queryStringParameters"]["localretention"]
            partition=event["queryStringParameters"]["partition"]
            rf=event["queryStringParameters"]["rf"]
            a=createTopic(bsrv,topicname,retention,localretention,partition,rf)
        
        elif whichfunction=='describetopic':
            topicname=event["queryStringParameters"]["topicname"]
            a=describeTopic(topicname,bsrv)
            
        return {
            'statusCode': 200,
            'body': json.dumps(a)
        }
    except Exception as e:
        # Return a 400 error to the client
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }
    

def getTopicConfig(topicname,bootstrapservers):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrapservers, client_id='test')
        topicconfig = admin_client.describe_configs(config_resources=[ConfigResource(ConfigResourceType.TOPIC, topicname)])
        config_list = str(topicconfig)
        return {
            'statusCode': 200,
            'body': json.dumps(config_list)
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }
        

def describeTopic(topicname,bootstrapservers):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrapservers, client_id='test')
        topicconfig = admin_client.describe_topics([topicname])
        return {
            'statusCode': 200,
            'body': topicconfig
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }
    
def getTopicList(bootstrapservers):
    try:
        admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrapservers, 
        client_id='test'
        )
        topic_list = []
        
        topiclist=admin_client.list_topics()
        return {
            'statusCode': 200,
            'body': json.dumps(topiclist)
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }

def createTopic(bootstrapservers,topicname,retention,localretention,partition,rf):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrapservers, client_id='test')
        
        if int(localretention) < int(retention):
            #Tiered storage enabled topic
            topic_configs={'retention.ms': int(retention),'remote.storage.enable':'true','local.retention.ms':int(localretention)}
        else:
            topic_configs={'retention.ms': int(retention)}
        
        
        topic_list = [
        NewTopic(
            name=topicname,
            num_partitions=int(partition),
            replication_factor=int(rf),
            #topic_configs={'retention.ms': int(retention),'remote.storage.enable':'true','local.retention.ms':int(localretention)}
            topic_configs=topic_configs
            
            )
        ]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        return {
            'statusCode': 200,
            'body': json.dumps("Topic :" + topicname + " created successfully")
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }


