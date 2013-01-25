18-Jan-2013
===========

- Installed EPD 7.2-2 for x64.
- Installed NStruct Instrument Manager package including NI-VISA 5.0.2, Notepad++ 5.7.0 and NSTRUCT 1.2.5.
- Installed IronPython 2.7.
- Modified ``%PATH%`` to add ``C:\Program Files (x86)\IronPython 2.7``.
- Installed ironpkg-1.0.0.
- Installed scipy and nose into IronPython environment using ironpkg.
- Installed GitHub for Windows.
- Encountered problem: ``nPython.exe`` (Python for .NET) will fail with R6034 due to missing WinSxS manifest.
- Installed pySerial using ``easy_install``. Tested.
- Tested IPython notebook.
 
22-Jan-2013
===========

- Followed Ian's instructions for installing Newport USB drivers.
- Connected Hallbach array via USB.
- Tested with ``python -m ni_engine.tools.conex_config`` that
  configuration could be read correctly using ``ConexCC``.

25-Jan-2013
===========

- Tested that ``ConexCC`` correctly controls linear and rotational motor movement.
  When used with the prototype NV Halbach array, all linear movement corresponds to the correct distance.
  Did not test software limits, as ``SR`` for each linear stage is set to ``25``, beyond the Halbach array's
  safe movement range.
- Disconnected Halbach array.
- Installed PyDAQmx_ 1.2.3 using ``easy_install``.
- Installed DAQmx_ 9.6 using NI Downloader. Warning observed about potential conflict with NStruct`s installation of NI-VISA 5.0.2.

.. _DAQmx: http://joule.ni.com/nidu/cds/view/p/id/3423/lang/en
.. _PyDAQmx: http://pypi.python.org/pypi/PyDAQmx
