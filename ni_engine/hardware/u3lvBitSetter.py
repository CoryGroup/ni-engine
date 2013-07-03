from abstractBitSetter import AbstractBitSetter
import u3
class U3LVBitSetter(AbstractBitSetter):

	def setPinsToAnalog(self,*pinNums):
		eioNum = 0
		fioNum = 0
		for x in pinNums:
			if x < 8:
				fioNum += 2**x
			else:
				eioNum += 2**(x-8)
		self.configIO(FIOAnalog=fioNum,EIOAnalog=eioNum)

	def setBitDir(self,*tuple):
		commands = map(lambda x: u3.bitDirWrite(IONumber=x[0],Direction=x[1]),tuple)
		return self.getFeedback(commands)

	def readAnalogPins(self,lst):
		return self.getFeedback(map(lambda x: u3.AIN(x),lst))

	def readDigitalPins(self,lst):
		raise self.getFeedback(map(lambda x: u3.BitDirRead(x),lst))
