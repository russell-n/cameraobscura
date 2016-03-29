Camera Obscura
==============

.. .. figure:: figures/vertov_eye.jpg

This was code written to run wireless tests inside an anechoic chamber. Signal attenuators control the signal-strength but I didn't write the attenuator controller code so that isn't included here. It could be used as a stand-alone iperf tester, but at that point it becomes a weak-version of other code I've written. I was originally going to make it compatible with some existing code that did the same thing but which had become un-maintainable but eventually realized that it would be better to re-create it instead. Because of this there's some inconsistency in the code-style as well as some un-used parts. The code is hosted on `github <https://github.com/russellnakamura/cameraobscura>`_.




Written Documentation
---------------------

This is the more organized documentation written outside of the code.

.. toctree::
   :maxdepth: 1

   User Documentation <documentation/user/index>
   Developer Documentation <documentation/developer/index>

Auto-Generated Documentation
----------------------------

These are the documents created from the source files.



.. toctree::
   :maxdepth: 1

   The Camera Obscura (Read Me) <readme.rst>
   The Log Setter <set_logger.rst>

.. toctree::
   :maxdepth: 1

   Attenuators <attenuators/index.rst>
   Client Connections <clients/index.rst>
   Commands <commands/index.rst>
   Common Code <common/index.rst>
   Hosts <hosts/index.rst>
   The Iperf Lexer <iperflexer/index.rst>
   RVR Plugin <plugins/index.rst>
   Rate-Vs-Range <ratevsrange/index.rst>
   Testing The Modules <tests/index.rst>
   Utility Modules <utilities/index.rst>



