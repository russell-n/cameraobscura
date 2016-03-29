from setuptools import setup, find_packages
setup(name='cameraobscura',
      author='anonymous',
      version="0.1.2",
      packages = find_packages(exclude=["setup", "__main__", "__init__"]),
      install_requires = ['pudb', 'iperflexer', 'theape',
                          'paramiko'],
      entry_points = """
[console_scripts]
rvr = cameraobscura.ratevsrange.main:main
"""
      )

#entry_points = 
#          """
#          [console_scripts]
#          roamingconfig = testsuites.AutomatedRoaming.main:main
#          rvrconfig = testsuites.AutomatedRVR.main:main
#          """

