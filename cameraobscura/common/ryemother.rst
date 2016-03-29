The Rye Mother
==============


The `Rye Mother <http://www.pitt.edu/~dash/gerchange.html#GrimmRyeMother>`_ gathers children.

.. figure:: figures/troll_changeling.jpg
   :align: center

   Source: `Wikipedia <http://en.wikipedia.org/wiki/File:En_kv%C3%A4ll_vid_midsommartid_gingo_de_med_Bianca_Maria_djupt_in_i_skogen2.jpg>`_

.. _cameraobscura-common-rye-mother-entry-points:
   
The Entry Points
----------------

The RyeMother uses entry points defined in the `setup.py` file. The entry_points use an ini-like format with the form::

    [group]
    name = module:object

In this case, the RyeMother wants to search the folder for class-definitions so the `object` is left out. As a concrete example, for the plugins, the entry points would look like this::

      entry_points = """
        [cameraobscura.plugins]
        plugins = cameraobscura.plugins
        """

.. note:: The actual `setup.py` has other entries, this is just the plugins entry.

The `[cameraobscura.plugins]` defines a group name and you can put multiple entries under it for other modules or objects. `plugins` is the name that is used to reference the `cameraobscura.plugins` module in the code.

.. _cameraobscura-common-rye-mother-dependecies:

Dependencies
------------

The RyeMother relies on several python modules.

.. csv-table:: Dependencies
   :header: Package, Source

   `pkgutil <https://docs.python.org/2/library/pkgutil.html>`_, python standard library
   `importlib <https://docs.python.org/2.7/library/importlib.html>`_, python standard library
   `os.path <https://docs.python.org/2/library/os.path.html>`_, python standard library
   `inspect <https://docs.python.org/2/library/inspect.html>`_, python standard library
   `pkg_resources <https://pythonhosted.org/setuptools/pkg_resources.html>`_ , setuptools

The methods used:

.. currentmodule:: pkg_resources
.. autosummary::
   :toctree: api

   pkg_resources.load_entry_point

.. currentmodule:: os.path
.. autosummary::
   :toctree: api

   dirname

.. currentmodule:: pkgutil
.. autosummary::
   :toctree: api

   iter_modules

.. currentmodule:: inspect
.. autosummary::
   :toctree: api

   getmembers

.. _tuna-commoncode-rye-mother-algorithm:

What the RyeMother Does
-----------------------

The RyeMother's __call__ method converts the parameters to a dictionary of class definition objects.

.. '

.. csv-table:: Call Parameters
   :header: Parameter, Description

   `parent`, The Base Class of the child-classes that we want to import
   `group`, Group name in the `entry_points` variable in `setup.py` (see :ref:`Entry Points <tuna-commoncode-rye-mother-entry-points>`)
   `name`, name of the module in the `entry_points` variable in `setup.py`
   `keyfunction`, function to transform the keys of the dictionary (default uses the actual class names)

The idea here is that to identify the classes that we're interested in we'll define them as children of a specific class.

.. uml::

   Parent <|-- Child_1
   Parent <|-- Child_2
   Parent <|-- Child_3

The `parent` parameter for the RyeMother is the actual class definition object. For example, if the user of the RyeMother did the following::

   from cameraobscura.plugins import BaseArguments

Then `BaseArguments` is what should be passed to the call and all the classes that inherit from it will be returned. If we defined `cameraobscura.plugins` as the group and  `plugins` as the name in the `setup.py` `entry_points` variable as mentioned :ref:`earlier <cameraobscura-common-rye-mother-entry-points>`, and we wanted to retrieve the `Run` class, we could use something like this::

   mother = RyeMother()
   children = mother(parent=BaseArguments, 
                     group='cameraobscura.plugins',
                     name='plugins')
   Run = children['Run']
   run_instance = Run()

The `keyfunction` is used to change the keys in the dictionary. One of the reasons that the RyeMother was created was so that classes could be auto-discovered and displayed for the users. Since the human-readable name might not always match the class-name, rather than forcing the classes to change their names, the `keyfunction` can be used to make a limited tranformation of the strings used as the keys.

To make them lower-cased you could use something like::

   keyfunction = lambda s: getattr(s, 'lower')()

The use of the gettattr might not seem intuitive, but since they recommend using string methods, I figured it'd be the best way. Another common transform might occur if the class names have a common suffix. Say they all have the suffix 'Arguments' and you don't want that in the dictionaries keys. You could do something like::

   keyfunction = lambda s: getattr(s, 'rstrip')('Arguments')   

This is the main path for the ``__call__``:

    #. Create a dictionary called `children`
    #. Import the package (folder) that contains the modules (files) that have the class definitions we want
    #. Get the package's directory
    #. Create a `prefix` using the module's package name
    #. Generate a list of module names within the imported module's directory and add the prefix to them (`<prefix>.<name>`)
    #. Import each of the module names from the previous step
    #. For each of the modules import all members that are children of the parent base-class
    #. For each member, if `keyfunction` is defined, transform its name
    #. For each member, add it to the children dictionary, using the name as a key and the class-definition object as the value

.. _cameraobscura-common-rye-mother-class:

The RyeMother Class
-------------------

.. module:: cameraobscura.common.ryemother 
.. autosummary::
   :toctree: api

   RyeMother
   RyeMother.__call__

.. note: In the event that the RyeMother needs to be used multiple time, the parameters can be set when it's constructed, but if they are passed into the call, then the passed-in parameters will override the instantiation parameters.

.. '

