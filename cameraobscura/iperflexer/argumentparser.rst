The Argument Parser
===================

.. currentmodule:: iperflexer.argumentparser

The ArgumentParser provides the main user interface to the *IperfLexer*.

* :ref:`The Arguments Class <argumentparser-arguments-class>`

* :ref:`Table of Command Line Arguments <argumentparser-command-line-arguments>`



.. _argumentparser-arguments-class:

The Arguments Class
-------------------

This was originally called the `ArgumentParser` but re-named `Arguments` so as not to be confused with the python `ArgumentParser`.

.. ifconfig:: repository != 'rtfd'

    .. uml::
    
       Arguments o-- argparse.ArgumentParser
       Arguments : Namespace parse_args()

.. autosummary::
   :toctree: api

   Arguments

Example Use::

   parser = Arguments()
   args = parser.parse_args()


.. _argumentparser-command-line-arguments:
   
Command Line Arguments
----------------------

The following are the accepted command-line-arguments. *Short Name* means a flag of the form ``-<short-name>`` and *Long Name* means a flag of the form ``--<long-name>``.

For example, to set the tee flag using the short-name and the voodoo flag using the long-name::

    pareiperf -t --voodoo

.. csv-table:: Command Line Arguments
   :header: Short Name, Long Name, Default, Description

   g, glob,None, If given read input from files instead of standard input
   m, maximum, 1000000, Values higher than this are set to 0
   s,save, False, if set and a glob was given will save the output to a file
   t, tee,False, If set send output to ``stderr``
   p,threads, 4,The number of threads (``-P`` iperf flag)
   u,units,Mbits,Units to convert the bandwidth to
   v,voodoo, False,If set adds the threads instead of using the SUM lines   
   ,pdb,False, If set start the ``pdb`` debugger
   ,pudb,False, If set start the ``pudb`` debugger (*nix only)
   

.. note:: The short-form of the `threads` argument is `p`, not `t`
   
