import serial, io, time, sys, win32con
import serial.tools.list_ports
import win32api as win32	

def getMonitorIDs():
	monitorIDs = []
	list = win32.EnumDisplayMonitors(None, None)
	for monitor in list:
		monitorIDs.append(int(win32.GetMonitorInfo(monitor[0])['Device'].replace('\\\\.\\DISPLAY', ''))-1)
	if len(monitorIDs) == 0: monitorIDs	= [0]
	return monitorIDs

def printAllScreen():
	monitorIDs = getMonitorIDs()
	print('Display IDs: [', end='')
	for monitorID in monitorIDs:
		print(monitorID + ', ', end='')
	print('] | ', end='')
	print('Default ID is: ' + monitorIDs[0])

def changeOrientation(display, direction):

	if(direction not in ['left', 'up', 'right', 'down']): direction = 'up'

	#Make the orentation to Win32 orientation format
	orientations = dict(zip(['left', 'up', 'right', 'down'], [1, 0, 3, 2]))

	device = win32.EnumDisplayDevices(None,display);
	settings = win32.EnumDisplaySettings(device.DeviceName,win32con.ENUM_CURRENT_SETTINGS)

	# New and Old orientation
	newOrientation = orientations[direction]
	oldOrientation = settings.DisplayOrientation

	# Check if the new orientation is perpendicular. Swap Height and Width if so.
	if(newOrientation + oldOrientation) % 2 == 1:
		width = settings.PelsWidth
		height = settings.PelsHeight
		settings.PelsWidth = height
		settings.PelsHeight = width
	settings.DisplayOrientation = newOrientation

	# Make the changes
	win32.ChangeDisplaySettingsEx(device.DeviceName,settings)
	return

def findArduinoPort():
	ports = list(serial.tools.list_ports.comports())
	for p in ports:
		if "Arduino" in p[1]:
			return p[0]
	return "COM1" # Try COM1

def main(argv):

	# Argument Defaults
	display = getMonitorIDs()[0]
	PORT = findArduinoPort()
	horizontal = 0
	prior = ""

	# Read from the command line
	i = 0
	while(i < len(argv)):

		# Normalize '--' to '-'
		if argv[i].startswith("--"):
			argv[i] = argv[i][1:]

		# Options
		if argv[i] == '-display':
			i += 1
			display = int(argv[i])

		elif argv[i] == '-on':
			i += 1
			if argv[i] == 'horizontal':
				horizontal = 1
			else:
				horizontal = 0

		elif argv[i] == '-port':
			i += 1
			PORT = argv[i]

		elif argv[i] == '-help':
			printAllScreen()
			return

		i += 1

	# Setup serial readers
	c = serial.Serial(PORT, 9600, timeout=1)
	if c.is_open == False:
		return
	else:
		cio = io.TextIOWrapper(io.BufferedRWPair(c, c))

	# Remove first garbage character/line
	cio.readline()

	# Begin Polling Arduino
	while(True):

		# Request State 1:Vertical 0:Horizontal - defaults
		cio.write(':')
		cio.flush()

		# Read State
		state = cio.readline().strip()

		changed = True
		if(prior == state):
			changed = False
		
		try:
			if(changed):
				# 1 => Vertical - default
				if(int(state) == horizontal):
					print("Horizontal")
					changeOrientation(display, 'up')
				# Horizontal != 1 - default
				else:
					print("Vertical")
					changeOrientation(display, 'left')
				prior = state

		except Exception as inst:
			print(type(inst))
			print(inst.args)    
			print(inst) 
			print("Issue, invalid state?")

if __name__== "__main__":
  main(sys.argv)