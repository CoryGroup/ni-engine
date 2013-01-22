18-Jan-2013
===========

 - Installed EPD 7.2-2 for x64.
 - Installed NStruct Instrument Manager package including NI-VISA 5.0.2, Notepad++ 5.7.0 and NSTRUCT 1.2.5.
 - Installed IronPython 2.7.
 - Modified %PATH% to add "C:\Program Files (x86)\IronPython 2.7".
 - Installed ironpkg-1.0.0.
 - Installed scipy and nose into IronPython environment using ironpkg.
 - Installed GitHub for Windows.

 - Encountered problem: nPython.exe (Python for .NET) will fail with R6034 due to missing WinSxS manifest.

 - Installed pySerial using easy_install. Tested.
 - Tested IPython notebook.
 
22-Jan-2013
===========

 - Followed Ian's instructions for installing Newport USB drivers.
 - Connected Hallbach array via USB.
 - Tested with ``python -m ni_engine.tools.conex_config`` that
   configuration could be read correctly using ``ConexCC``.