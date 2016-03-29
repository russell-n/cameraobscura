Feature: AttenuationPluginConfiguration
 Scenario: User creates AttenuationPluginConfiguration
  Given an AttenuationPluginConfiguration
  When the AttenuationPluginConfiguration is checked
  Then it is an ape SubConfiguration
  And it has the AttenuationPluginConfiguration defaults

 Scenario: User sets AttenuationPluginConfiguration values
  Given an AttenuationPluginConfiguration with values
  When the AttenuationPluginConfiguration values are checked
  Then the AttenuationPluginConfiguration values are correct
  And the AttenuationPlugin values are correct

