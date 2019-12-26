from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters
import os
import azure
import azure.mgmt.monitor.models
import azure.mgmt.subscription.operations


class StorageServices:
    def __init__(self, client):
        self.client = client

    def check_access_to_anonymous_users(self):
        issues = []
        try:
            subscription_id = ""
            credentials = ServicePrincipalCredentials(
                client_id=os.environ['AZURE_CLIENT_ID'],
                secret=os.environ['AZURE_CLIENT_SECRET'],
                tenant=os.environ['AZURE_TENANT_ID']
            )
            subscription_client = SubscriptionClient(credentials)
            subscription_list = subscription_client.subscriptions.list()
            for i in subscription_list:
                try:
                    subscription_id = i.subscription_id
                    resource_client = ResourceManagementClient(credentials, subscription_id)
                    storage_client = StorageManagementClient(credentials, subscription_id)

                    for item in storage_client.storage_accounts.list():
                        for resource in resource_client.resource_groups.list():
                            response = storage_client.blob_containers.list(resource_group_name=resource.name,
                                                                           account_name=item.name)
                            list_container_items = azure.mgmt.storage.models.ListContainerItems().from_dict(response).value
                            for container in list_container_items:
                                temp = dict()
                                temp["region"] = resource.location
                                if container.public_access.value == "Container":
                                    temp["status"] = "Fail"
                                    temp["resource_name"] = container.name
                                    temp["resource_id"] = ""
                                    temp["problem"] = "Container %s in storage account %s has access to anonymous users".\
                                                        format(container.name, resource.name)
                                else:
                                    temp["status"] = "Pass"
                                    temp["resource_name"] = container.name
                                    temp["resource_id"] = ""
                                    temp["problem"] = "Container %s in storage account %s doesn't allow access to anonymous users".\
                                                        format(container.name, resource.name)
                                issues.append(temp)
                except Exception as e:
                    print(str(e))
                    continue;
        except Exception as e:
            print(str(e));
        finally:
            return issues

    def restrict_default_network_access(self):
        issues = []
        try:
            subscription_id = ""
            credentials = ServicePrincipalCredentials(
                client_id=os.environ['AZURE_CLIENT_ID'],
                secret=os.environ['AZURE_CLIENT_SECRET'],
                tenant=os.environ['AZURE_TENANT_ID']
            )
            subscription_client = SubscriptionClient(credentials)
            subscription_list = subscription_client.subscriptions.list()
            for i in subscription_list:
                subscription_id = i.subscription_id
                storage_client = StorageManagementClient(credentials, subscription_id)

                for item in storage_client.storage_accounts.list():
                    temp = dict()
                    temp["region"] = item.location
                    # item.id
                    if item.network_rule_set.default_action.value == "Allow":
                        temp["status"] = "Fail"
                        temp["resource_name"] = item.name
                        temp["resource_id"] = ""
                        temp["problem"] = "Storage Account {} is accessible from default network". format(item.name)
                    else:
                        temp["status"] = "Pass"
                        temp["resource_name"] = item.name
                        temp["resource_id"] = ""
                        temp["problem"] = "Storage Account {} is not accessible from default network".format(item.name)
                    issues.append(temp)

        except Exception as e:
            print(str(e));
        finally:
            return issues

    def enable_secure_transfer(self):
        issues = []
        try:
            subscription_id = ""
            credentials = ServicePrincipalCredentials(
                client_id=os.environ['AZURE_CLIENT_ID'],
                secret=os.environ['AZURE_CLIENT_SECRET'],
                tenant=os.environ['AZURE_TENANT_ID']
            )
            subscription_client = SubscriptionClient(credentials)
            subscription_list = subscription_client.subscriptions.list()
            for i in subscription_list:
                subscription_id = i.subscription_id
                storage_client = StorageManagementClient(credentials, subscription_id)

                for item in storage_client.storage_accounts.list():
                    temp = dict()
                    temp["region"] = item.location
                    if not item.enable_https_traffic_only:
                        temp["status"] = "Fail"
                        temp["resource_name"] = item.name
                        temp["resource_id"] = ""
                        temp["problem"] = "Secure data transfer is not enabled for Storage Account {} ".format(item.name)
                    else:
                        temp["status"] = "Pass"
                        temp["resource_name"] = item.name
                        temp["resource_id"] = ""
                        temp["problem"] = "Secure data transfer is enabled for Storage Account {} ".format(item.name)
                    issues.append(temp)
        except Exception as e:
            print(str(e));
        finally:
            return issues

    def check_trusted_services_access(self):
        issues = []
        try:
            subscription_id = ""
            credentials = ServicePrincipalCredentials(
                client_id=os.environ['AZURE_CLIENT_ID'],
                secret=os.environ['AZURE_CLIENT_SECRET'],
                tenant=os.environ['AZURE_TENANT_ID']
            )
            subscription_client = SubscriptionClient(credentials)
            subscription_list = subscription_client.subscriptions.list()
            for i in subscription_list:
                subscription_id = i.subscription_id
                storage_client = StorageManagementClient(credentials, subscription_id)

                for item in storage_client.storage_accounts.list():
                    temp = dict()
                    temp["region"] = item.location
                    if item.network_rule_set.bypass is None:
                        temp["status"] = "Fail"
                        temp["resource_name"] = item.name
                        temp["resource_id"] = ""
                        temp["problem"] = "Trusted Microsoft Services are not allowed to access the Storage Account {} ".format(
                            item.name)
                    else:
                        temp["status"] = "Pass"
                        temp["resource_name"] = item.name
                        temp["resource_id"] = ""
                        temp[
                            "problem"] = "Trusted Microsoft Services are allowed to access the Storage Account {} ".format(
                            item.name)
                    issues.append(temp)
        except Exception as e:
            print(str(e));
        finally:
            return issues

    def regenerate_storage_account_keys(self):
        try:
            subscription_id = ""
            credentials = ServicePrincipalCredentials(
                client_id=os.environ['AZURE_CLIENT_ID'],
                secret=os.environ['AZURE_CLIENT_SECRET'],
                tenant=os.environ['AZURE_TENANT_ID']
            )
            subscription_client = SubscriptionClient(credentials)

            subscription_list = subscription_client.subscriptions.list()
            for i in subscription_list:
                subscription_id = i.subscription_id
                x = subscription_client.subscriptions.get(subscription_id= subscription_id)
                storage_client = StorageManagementClient(credentials, subscription_id)

                for item in storage_client.storage_accounts.list():
                    print(item.name)
                    temp = item.id.split("resourceGroups")
                    resource_group = temp[1].split("/")[1]
                    filters = "resourceGroupName eq '{}' ".format(resource_group)
        except Exception as e:
            print(str(e));