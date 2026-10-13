@description('Actual globally unique factory name; Azure validates naming rules.')
param factoryName string
param location string = resourceGroup().location
@allowed(['dev','test','prod'])
param environment string = 'dev'
resource factory 'Microsoft.DataFactory/factories@2018-06-01' = {
  name: factoryName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  tags: {
    environment: environment
  }
  properties: {}
}
output factoryId string = factory.id
output principalId string = factory.identity.principalId
// Source data grants, IR hosts, network/private endpoints, vault and diagnostics
// are separate platform prerequisites; application assets come from exported ARM.
