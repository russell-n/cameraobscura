Feature: RVR Plugin for the APE
 Scenario: User builds the RVR Plugin
  Given an instance of the RVR Plugin
  When the RVR Plugin is checked
  Then the RVRPlugin is an APE Plugin

 Scenario: User builds the minimal RVR Configuration
  Given an instance of the minimal RVRConfiguration 
  When the RVRConfiguration is checked
  Then RVRConfiguration is instance of ape's BaseConfiguration
  And RVRConfiguration has the values set by the user
  And RVRConfiguration has the default values
  
 Scenario: User builds the RVR Configuration with extra iperf values
  Given an instance of the RVRConfiguration with extra iperf values
  When the RVRConfiguration is checked for extra iperf values
  Then the RVRConfiguration has the extra iperf values
  
