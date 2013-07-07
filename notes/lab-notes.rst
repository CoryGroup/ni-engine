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

12-April-2013
=============

- Installed packages for use with ``gpibusb-comm_code``::

    > easy_install flufl.enum==4.0
	> easy_install pyvisa
	> easy_install quantities
	
23-April-2013
=============

- Installed unofficial binary for PyOpenCL found at http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl.
- Installed pytools, as required by PyOpenCL::

    > easy_install pytools
    
- Tested that the demonstration program shipped with PyOpenCL works::

    In [1]: import pyopencl as cl
       ...: import numpy
       ...: import numpy.linalg as la
       ...: 
       ...: a = numpy.random.rand(50000).astype(numpy.float32)
       ...: b = numpy.random.rand(50000).astype(numpy.float32)
       ...: 
       ...: ctx = cl.create_some_context()
       ...: queue = cl.CommandQueue(ctx)
       ...: 
       ...: mf = cl.mem_flags
       ...: a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
       ...: b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
       ...: dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)
       ...: 
       ...: prg = cl.Program(ctx, """
       ...:     __kernel void sum(__global const float *a,
       ...:     __global const float *b, __global float *c)
       ...:     {
       ...:       int gid = get_global_id(0);
       ...:       c[gid] = a[gid] + b[gid];
       ...:     }
       ...:     """).build()
       ...: 
       ...: prg.sum(queue, a.shape, None, a_buf, b_buf, dest_buf)
       ...: 
       ...: a_plus_b = numpy.empty_like(a)
       ...: cl.enqueue_copy(queue, a_plus_b, dest_buf)
       ...: 
       ...: print la.norm(a_plus_b - (a+b))
    0.0

 21-May-2013
 ===========
 
 - Installed LabJack UD and LabJackPython from http://labjack.com/support/labjackpython.
 - Installed stand-alone LJTickDAC example from http://labjack.com/support/accessories/ljtickdac.
 - Installed Evince reader from https://live.gnome.org/Evince/Downloads.
 - Tested that LJTickDAC connected to FIO4/5 block produced correct output, up to small calibration errors.
 - Installed example for temp/humidity probe http://labjack.com/support/ei-1050/sample-windows.
 - Tested that temp/humidity probe works when connected as instructed in the example application.
 
 10-June-2013
 ===========
 
 - Installed Xerox Workstation 5335 drivers, to enable printing. Can be found at http://www.support.xerox.com/support/workcentre-5300-series/file-download/enus.html?operatingSystem=win7x64&fileLanguage=en&contentId=117759&from=downloads&viewArchived=false
 - Updated LabJack Firmware
 
 13-June-2013 
 ============

 - Installed pip via http://www.lfd.uci.edu/~gohlke/pythonlibs/#distribute to allow easy installation of libraries 
 - Installed text editor sublime-text-2  
 17-June-2013
 -Installed Microsoft powerpoint viewer
 -Installed ComSolve
 
 04-July-2013
 ============

 - Installed Microsoft office for excel
 - Installed R and R studio