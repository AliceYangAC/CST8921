# Lab 2 – Cloud Security

## Alice Yang 041200019


## Task 1: Azure Policy - AlloId Locations

![alt text](images/image.png)
![alt text](images/image-1.png)
![alt text](images/image-2.png)
![alt text](images/image-3.png)
![alt text](images/image-4.png)

Azure Policy allows us to set governance rules over resources deployed in the subscription scope. Here, for Azure for Students sub, I set a policy that only Canada Central resources can be deployed.

## Task 2: VNet (Canada Central)

![alt text](images/image-5.png)
![alt text](images/image-6.png)
![alt text](images/image-7.png)

I deployed a VNet in Canada Central with default network settings.

## Task 3: Subnets & Microsoft.Storage

![alt text](images/image-8.png)
![alt text](images/image-11.png)
![alt text](images/image-9.png)
![alt text](images/image-10.png)

I created two subnets, one private, and one public. The private subnet will be secured to only allow outbound access to a service endpoint to an Azure Storage Account via the tag `Microsoft.Storage`. The public subnet does not have a service endpoint.

## Task 4: NSGs

![alt text](images/image-12.png)
![alt text](images/image-13.png)
![alt text](images/image-14.png)

Next, I created a NSG to configure for our private subnet and later public subnet.

## Task 5-6: NSG Rules (Private Subnet, Public RDP Access)

![alt text](images/image-15.png)
![alt text](images/image-16.png)
![alt text](images/image-17.png)
![alt text](images/image-18.png)
![alt text](images/image-21.png)
![alt text](images/image-19.png)
![alt text](images/image-20.png)
![alt text](images/image-22.png)

I configured the NSGs with set outbound and inbound rules appropriate for the subnet. The private NSG explicitly allows only outbound traffic to Storage tags, and denies traffic to the Internet. This follows Zero Trust principles, enforcing security. The public NSG allows inbound RDP from port 3389 TCP protocol.

## Task 7: Storage Account & File Share

![alt text](images/image-23.png)
![alt text](images/image-24.png)
![alt text](images/image-25.png)
![alt text](images/image-26.png)

I then created a Storage Account with the Networking settings to enable access only from selected networks, the previously created `private-subnet` that has a NSG configured to only allow outbound traffic to this Storage Account.

Unfortunately due to region restrictions, I am unable to create an Azure File Share since Microsoft restricted my regions for resource deployment only for ["eastus2","Istus3","Istus2","canadacentral","northcentralus"], none of which are available regions for File Share. As a result, I am unable to continue the lab until an alternative option is found. It also directly contradicts with the policy set in Task 1.

## Delete Resources

![alt text](images/image-27.png)