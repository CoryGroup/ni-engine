===================
CONEX-CC Controller
===================

Windows Driver Installation
===========================

The following are generic instructions for installing devices with FTDI USB-RS232 chips in them.

1) Plug USB stuff in
2) Download drivers from the manufacturer of the chip (in this case, FTDI's FT232RL)
3) Download USBView (made by microsoft, available on FTDI website)
4) Use USBView to determine the PID and VID of the chip (in this case, PID=idProduct=3002,VID=idVendor=104D)
5) Locate all .inf files in the drivers folder. Replace PID and VID numbers with the ones you found in part 4. In the case that there exist multiple lines with different PID's, figure out which PID the chip comes with by default (found here in this case: http://www.ftdichip.com/Support/Documents/TechnicalNotes/TN_100_USB_VID-PID_Guidelines.pdf), and get rid of the other lines. In the CONNEX-CC case, the chip is the 232RL version, which has PID 6001.
6) Go to the Windows Device Manager, right click the "unknown" software, and select Update Driver
7) Select the driver folder you downloaded with modified INF files
8) It should work.
9) More things will pop up in the "Other Devices" section of the Device Manager. Repeat 6, 7, 8 on these.

Command Set
===========

- Queries on configuration parameters are supported in the ``NOT REGISTERED`` state, despite documentation in the manual.
 
