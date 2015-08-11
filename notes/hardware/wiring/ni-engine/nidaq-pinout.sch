EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:national-instruments
EELAYER 27 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "8 aug 2013"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L NI_6602 U?
U 1 1 52040EC6
P 3000 3350
F 0 "U?" H 2050 4850 60  0001 C CNN
F 1 "NI_6602" H 3050 6000 60  0000 C CNN
F 2 "~" H 2050 4850 60  0000 C CNN
F 3 "~" H 2050 4850 60  0000 C CNN
	1    3000 3350
	1    0    0    -1  
$EndComp
$Comp
L BNC CH
U 1 1 52040ED5
P 6100 1000
F 0 "CH 1" H 6110 1120 60  0000 C CNN
F 1 "BNC" V 6210 940 40  0000 C CNN
F 2 "~" H 6100 1000 60  0000 C CNN
F 3 "~" H 6100 1000 60  0000 C CNN
	1    6100 1000
	1    0    0    -1  
$EndComp
$Comp
L BNC CH
U 1 1 52040EE4
P 6650 1000
F 0 "CH 3" H 6660 1120 60  0000 C CNN
F 1 "BNC" V 6760 940 40  0000 C CNN
F 2 "~" H 6650 1000 60  0000 C CNN
F 3 "~" H 6650 1000 60  0000 C CNN
	1    6650 1000
	1    0    0    -1  
$EndComp
$Comp
L BNC CH
U 1 1 52040EF3
P 7200 1000
F 0 "CH 5" H 7210 1120 60  0000 C CNN
F 1 "BNC" V 7310 940 40  0000 C CNN
F 2 "~" H 7200 1000 60  0000 C CNN
F 3 "~" H 7200 1000 60  0000 C CNN
	1    7200 1000
	1    0    0    -1  
$EndComp
$Comp
L BNC CH
U 1 1 52040F02
P 7800 1000
F 0 "CH 7" H 7810 1120 60  0000 C CNN
F 1 "BNC" V 7910 940 40  0000 C CNN
F 2 "~" H 7800 1000 60  0000 C CNN
F 3 "~" H 7800 1000 60  0000 C CNN
	1    7800 1000
	1    0    0    -1  
$EndComp
$Comp
L BNC CH
U 1 1 52040F11
P 6100 1650
F 0 "CH 2" H 6110 1770 60  0000 C CNN
F 1 "BNC" V 6210 1590 40  0000 C CNN
F 2 "~" H 6100 1650 60  0000 C CNN
F 3 "~" H 6100 1650 60  0000 C CNN
	1    6100 1650
	1    0    0    -1  
$EndComp
$Comp
L BNC CH
U 1 1 52040F20
P 6650 1650
F 0 "CH 4" H 6660 1770 60  0000 C CNN
F 1 "BNC" V 6760 1590 40  0000 C CNN
F 2 "~" H 6650 1650 60  0000 C CNN
F 3 "~" H 6650 1650 60  0000 C CNN
	1    6650 1650
	1    0    0    -1  
$EndComp
$Comp
L BNC CH
U 1 1 52040F2F
P 7200 1650
F 0 "CH 6" H 7210 1770 60  0000 C CNN
F 1 "BNC" V 7310 1590 40  0000 C CNN
F 2 "~" H 7200 1650 60  0000 C CNN
F 3 "~" H 7200 1650 60  0000 C CNN
	1    7200 1650
	1    0    0    -1  
$EndComp
$Comp
L BNC CH
U 1 1 52040F3E
P 7800 1650
F 0 "CH 8" H 7810 1770 60  0000 C CNN
F 1 "BNC" V 7910 1590 40  0000 C CNN
F 2 "~" H 7800 1650 60  0000 C CNN
F 3 "~" H 7800 1650 60  0000 C CNN
	1    7800 1650
	1    0    0    -1  
$EndComp
Wire Wire Line
	950  5250 1300 5250
Wire Wire Line
	950  2850 950  6200
Wire Wire Line
	950  4800 1300 4800
Wire Wire Line
	5100 3450 4750 3450
Wire Wire Line
	5100 6200 5100 1050
Wire Wire Line
	950  6200 5100 6200
Connection ~ 950  5250
Wire Wire Line
	1300 2850 950  2850
Connection ~ 950  4800
Wire Wire Line
	4750 2400 5100 2400
Connection ~ 5100 3450
Wire Wire Line
	4750 1950 5100 1950
Connection ~ 5100 2400
Wire Wire Line
	4750 1500 5100 1500
Connection ~ 5100 1950
Connection ~ 5100 1500
Text Label 5750 1000 0    60   ~ 0
J7
Text Label 5800 850  1    60   ~ 0
J7
Text Label 5900 800  1    60   ~ 0
J7
Text GLabel 5950 1000 0    60   Input ~ 0
J7
Text GLabel 1300 4950 0    60   Input ~ 0
J7
Text GLabel 5950 1650 0    60   Input ~ 0
J34
Text GLabel 1300 900  0    60   Input ~ 0
J34
Text GLabel 6500 1000 0    60   Input ~ 0
J31
Text GLabel 6500 1650 0    60   Input ~ 0
J28
Text GLabel 7050 1000 0    60   Input ~ 0
J25
Text GLabel 7050 1650 0    60   Input ~ 0
J22
Text GLabel 7650 1000 0    60   Input ~ 0
J52
NoConn ~ 7650 1650
NoConn ~ 7800 1850
Text GLabel 6100 1200 3    60   Input ~ 0
J41
Text GLabel 6100 1850 3    60   Input ~ 0
J68
Text GLabel 6650 1200 3    60   Input ~ 0
J65
Text GLabel 6650 1850 3    60   Input ~ 0
J62
Text GLabel 7200 1200 3    60   Input ~ 0
J59
Text GLabel 7200 1850 3    60   Input ~ 0
J55
Text GLabel 7800 1200 3    60   Input ~ 0
J18
Text GLabel 4750 4950 2    60   Input ~ 0
J41
Text GLabel 4750 900  2    60   Input ~ 0
J68
Text GLabel 4750 1350 2    60   Input ~ 0
J65
Wire Wire Line
	4750 1050 5100 1050
Text GLabel 4750 1800 2    60   Input ~ 0
J62
Text GLabel 4750 2250 2    60   Input ~ 0
J59
Text GLabel 4750 2850 2    60   Input ~ 0
J55
Text GLabel 4750 3300 2    60   Input ~ 0
J52
Text GLabel 1300 1350 0    60   Input ~ 0
J31
Text GLabel 1300 1800 0    60   Input ~ 0
J28
Text GLabel 1300 2250 0    60   Input ~ 0
J25
Text GLabel 1300 2700 0    60   Input ~ 0
J22
$EndSCHEMATC
