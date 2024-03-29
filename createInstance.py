import boto3
import time
from botocore.exceptions import ClientError
import logging
import os

ec2 = boto3.resource('ec2')

# # maintain a list of instances and their information
# instance_list = []


def create_instance(imageID, minCount, maxCount, type, keyPair, size):
    instance_list = []
    try:
        # create EBS volume
        # bdms = create_block_device_mappings(size)

        # create instance
        instances = ec2.create_instances(
            ImageId=imageID,
            MinCount=minCount,
            MaxCount=maxCount,
            InstanceType=type,
            KeyName=keyPair,
            BlockDeviceMappings=[{"DeviceName": "/dev/xvda", "Ebs": {"VolumeSize": size}}]
        )
    except ClientError as e:
        logging.error(e)
        return None
    for instance in instances:
        start_time = time.time()
        while instance.state['Name'] != 'running':
            time.sleep(5)
            print('instance not up yet')
            current_time = time.time()
            time_passed = current_time - start_time
            print('time passed: ' + str(time_passed) + ' seconds')
            # if time over 5 minutes, abort
            if time_passed >= 300:
                print('Time limit exceeds! Please try again.')
                return None
            instance.load()
        print('instance running!')

        # # add created instance id to instance list
        # instance_dict = {'id': instance.id}
        # instance_list.append(instance_dict)

        instance_list.append({'ID': instance.id, 'Type': instance.instance_type, 'Public_IP': instance.public_ip_address})
    return instance_list


def main():
    image_id = 'ami-0b69ea66ff7391e80'  # image id indicates AMI
    instance_type = 't2.micro'  # instance type
    keypair_name = 'MKeyPair'  # key file
    minCount = 1  # min number of instances to create
    maxCount = 5  # max number of instances to create
    size = 10  # size of root EBS volume in GiB
    user_name = 'ec2-user'

    # create the instance
    instance_information = create_instance(image_id, minCount, maxCount, instance_type, keypair_name, size)
    print(instance_information)

    # cmd = 'ssh -i ' + keypair_name + '.pem ' + user_name + '@' + instance_information[-1]
    # print(cmd)


# os.system(cmd)


if __name__ == '__main__':
    main()
