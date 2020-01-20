base_url = "https://management.azure.com"
subscriptions_list_url = "https://management.azure.com/subscriptions"
resource_group_list_url = "https://management.azure.com/subscriptions/{}/resourcegroups"
storage_accounts_list_url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.Storage/storageAccounts"
container_list_url = "https://management.azure.com/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Storage/storageAccounts/{}/blobServices/default/containers"
role_definitions_list_url = "https://management.azure.com/{}/providers/Microsoft.Authorization/roleDefinitions"
log_profile_list_url = "https://management.azure.com/subscriptions/{}/providers/microsoft.insights/logprofiles"
key_vault_list_url = "https://management.azure.com/subscriptions/{}/resources?$filter=resourceType eq 'Microsoft.KeyVault/vaults'"
monitor_diagnostic_url= "https://management.azure.com/{}/providers/microsoft.insights/diagnosticSettings"
monitor_activity_log_url = "https://management.azure.com/subscriptions/{}/providers/microsoft.insights/eventtypes/management/values"
policy_assignments_url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.Authorization/policyAssignments/SecurityCenterBuiltIn"
security_contacts_url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.Security/securityContacts"
auto_provision_url = " https://management.azure.com/subscriptions/{}/providers/Microsoft.Security/autoProvisioningSettings"
pricing_url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.Security/pricings"
postgres_server_list_url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.DBforPostgreSQL/servers"
sql_server_list_url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.Sql/servers"
mysql_server_list_url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.DBforMySQL/servers"

check_mapping = {
    'CEN_AZ_2': 'CEN_AZ_2','CEN_AZ_3': 'CEN_AZ_3()'
}