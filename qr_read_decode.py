# importing necessary packages
from PIL import ImageTk
from PIL import Image
import tkinter as tki
import threading
import imutils
import cv2
from pyzbar import pyzbar
from imutils.video import VideoStream



class PhotoApp:
	def __init__(self, vs):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
		self.vs = vs
		self.frame = None
		self.thread = None
		self.stopEvent = None
		# initialize the root window and image panel
		self.root = tki.Tk()
		self.panel = None
		self.root.geometry('400x400')
		self.barcodeData = None
		self.root.resizable(False, False)
		# add text
		# this creates 'Label' widget for Registration Form and uses place() method.
		label_0 = tki.Label(self.root, text="Scan the QR Code...", width=20, font=("bold", 12))
		# place method in tkinter is  geometry manager it is used to organize widgets by placing them in specific position
		label_0.place(x=80, y=20)
		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()
		# set a callback to handle when the window is closed
		self.root.wm_title("QR scanner")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		try:
			# keep looping over frames until we are instructed to stop
			while not self.stopEvent.is_set():
				# grab the frame from the video stream and resize it to
				# have a maximum width of 300 pixels
				self.frame = self.vs.read()
				self.barcodeData = None
				self.frame = imutils.resize(self.frame, width=350)
				self.barcodes = pyzbar.decode(self.frame) 
				# print(self.barcodes)
				# if Qr decoded display on the screen
				if len(self.barcodes)!= 0: 
					self.barcodeData = self.barcodes[0].data.decode("utf-8")
					# print(self.barcodeData)
					self.stopEvent.set()
					self.vs.stop()
					self.panel.destroy()
					label_0 = tki.Label(self.root, text="Decode Data", width=20, font=("bold", 12))
					label_0.place(x=80, y=20)
					# Create text widget and specify size. 
					T = tki.Text(self.root, height =10,width=40, bg="lightgray")     
					T.pack() 
					T.insert("2.0", "Type:"+ self.barcodes[0].type + "\n") 
					T.insert("2.0", "Data:"+self.barcodeData) 
					T.place(x=40, y=90)				
				# OpenCV represents images in BGR order; however PIL
				# represents images in RGB order, so we need to swap
				# the channels, then convert to PIL and ImageTk format
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				# img_ref = image.copy()
				image = cv2.rectangle(image, (20,20), (280,240), (0,255,0), 1)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
						
				# if the panel is not None, we need to initialize it
				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.image = image
					self.panel.pack(side="left", padx=50, pady=30)		
				# otherwise, simply update the panel
				else:
					self.panel.configure(image=image)
					self.panel.image = image
		except Exception as e :
			print("[INFO] caught a RuntimeError",e)
	
	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()


# calling class and objects
vs = VideoStream(0).start()
pba = PhotoApp(vs)
pba.root.mainloop()

