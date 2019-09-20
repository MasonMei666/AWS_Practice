import boto3
import time
from botocore.exceptions import ClientError
import logging
import os

from createInstance import create_instance

ec2 = boto3.resource('ec2')


def retrieve_instances_by_filter(filter_name, filter_values):
    instances = ec2.instances.filter(Filters=[{'Name': filter_name, 'Values': filter_values}])


def retrieve_all_running_instances():
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    return instances


def stop_instance(instance_ids):
    ec2.instances.filter(InstanceIds=instance_ids).stop()


def terminate_instances(instance_ids):
    ec2.instances.filter(InstanceIds=instance_ids).terminate()


def main():
    # stop all running instances
    instances = retrieve_all_running_instances()
    instances.stop()


if __name__ == '__main__':
    main()
