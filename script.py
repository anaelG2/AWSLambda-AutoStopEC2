import boto3
import logging
from datetime import datetime

now = datetime.now() 
timeNowFormattedString = now.strftime("%H:%M")
timeFormattedDate=datetime.strptime(timeNowFormattedString,'%H:%M')


#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [{
            'Name': 'tag:AutoOff',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    #filter the instances
    instances = ec2.instances.filter(Filters=filters)
    
    #locate all running instances
    RunningInstances = [instance.id for instance in instances]

    #get tags with stop hour
    for instance in instances:
        for tag in instance.tags:
            if "shutdownHour" in tag['Key']:
                tagDate=datetime.strptime(tag['Value'],'%H:%M')
                if timeFormattedDate > tagDate:
                    shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
                    print(shuttingDown)
                    print("L'instance {} a été shutdown".format(instance.id))
