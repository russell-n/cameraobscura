SimpleClient
============

This is a wrapper around paramiko's `SSHClient` that sets some flags to avoid host-key errors. The following are roughly equivalent.

.. '

SSHClient::

   c = SSHClient()
   c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   c.load_system_host_keys()
   c.connect(hostname='192.168.10.24', username='allion')
   stdin, stdout, stderror = c.exec_command('ls')

SimpleClient::

   c = SimpleClient(hostname='192.168.10.24', username='allion')
   stdin, stdout, stderr = c.exec_command('ls')

Contents:

    * :ref:`Paramiko SSHClient <simpleclient-paramiko>`
    * :ref:`ConnectionError <simpleclient-connectionerror>`
    * :ref:`The SimpleClient <simpleclient>`

.. _simpleclient-paramiko:   

Paramiko's SSHClient
--------------------

This is some basic documentation for the SSHClient's methods. Only some of them are re-implemented by the SimpleClient (because it's simple), but the getattr is implemented so you can call the paramiko methods and they should work, but the errors will be different from the SimpleClient (they will be ``socket`` or ``paramiko`` errors) so you have to trap them.

.. '

.. currentmodule:: paramiko
.. autosummary::
   :toctree: api

   paramiko.SSHClient
   paramiko.SSHClient.close
   paramiko.SSHClient.connect
   paramiko.SSHClient.exec_command
   paramiko.SSHClient.get_host_keys
   paramiko.SSHClient.get_transport
   paramiko.SSHClient.invoke_shell
   paramiko.SSHClient.load_host_keys
   paramiko.SSHClient.open_sftp
   paramiko.SSHClient.save_host_keys
   paramiko.SSHClient.set_log_channel
   paramiko.SSHClient.set_missing_host_key_policy

.. note:: set_missing_host_key_policy and load_system_host_keys is called when the client is created, so you shouldn't call it. The only extra methods you will likely ever use are ``invoke_shell`` and ``open_sftp``. Otherwise you might as well use the SSHClient directly. The purpose of this module was to make it easier, not to re-do everything.

.. '   




.. _simpleclient-connectionerror:

The ConnectionError
-------------------

This is just a sub-class of the `CameraobscuraError` so anything that traps that will catch it.

.. uml::

   CameraobscuraError <|-- ConnectionError

.. currentmodule:: cameraobscura.clients.simpleclient
.. autosummary::
   :toctree: api

   ConnectionError




.. _simpleclient:

SimpleClient
------------

.. autosummary::
   :toctree: api

   SimpleClient
   SimpleClient.exec_command
   SimpleClient.client
   SimpleClient.__getattr__
   SimpleClient.__str__
   SimpleClient.close

.. uml::

   SimpleClient -|> BaseClient
   SimpleClient o-- SSHClient
   SimpleClient : client
   SimpleClient : hostname
   SimpleClient : username
   SimpleClient : password
   SimpleClient : port
   SimpleClient : timeout
   SimpleClient : exec_command(command, timeout)
   SimpleClient : __str__()
   SimpleClient : close()




.. warning:: I'm using *args, **kwargs when connecting to the client so anything other than hostname, username and timeout will be passed in that way, but the string representation (``__str__``) expects the kwargs dictionary to have 'port' and 'password' arguments -- to be safe use keyword arguments, not positional arguments when instantiating the SimpleClient.

.. '






