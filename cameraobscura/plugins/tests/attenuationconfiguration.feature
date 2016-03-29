Feature: AttenuationConfiguration
 Scenario: User creates AttenuationConfiguration
  Given an AttenuationConfiguration
  When the AttenuationConfiguration is checked
  Then it is an ape SubConfiguration
  And it has the AttenuationConfiguration defaults

 Scenario: User sets AttenuationConfiguration values
  Given an AttenuationConfiguration with values
  When the AttenuationConfiguration values are checked
  Then the AttenuationConfiguration values are correct

