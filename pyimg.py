import pyimgur
import time
import os
import win32gui,  win32ui,  win32con, win32api
from PIL import Image
import winsound
import sys
import pythoncom, pyHook
import threading
import urllib2
import random
import copy

#settings:
cid = "5976c17ac696c9b" #client id
sound = True #beep if error
skey = 'F9' #screenshot key
lkey = 'F10' #location key
comp = 0 #compression?
ptimeout = 30 #time out 
wipe = True #for location
ltime = time.time() #last time
btime = 1.0 #min time between consecutive

def redirect(ourl, nurl): #tinyurl api
	turl = "http://tinyurl.com/create.php?&url="+ourl+"&alias="+nurl
	urllib2.urlopen(turl) #visit site

def randstring(len = 12):
	return str(random.randint(0,10**len-1))

def uploadimg(path, id = cid, title = ''):
	im = pyimgur.Imgur(id)
	uploaded_image = im.upload_image(path, title=title)
	return uploaded_image.link

def toclipboard(text):
	os.system('echo ' + text.strip() + '| clip')

def reformat(bmpinfo, bmpstr, filename, typ = comp):
	im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
	if not(typ):
		im.save(filename, format = 'png')
	else:
		im.save(filename, format = 'jpeg', quality = typ)
	
def screenshot(filename, x1 = None, y1 = None, x2 = None, y2 = None):
	SM_XVIRTUALSCREEN = 76
	SM_YVIRTUALSCREEN = 77
	SM_CXVIRTUALSCREEN = 78
	SM_CYVIRTUALSCREEN = 79
	#
	w = vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
	h = vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
	l = vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
	t = vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
	if None not in [x1, y1, x2, y2]:
		w = x2-x1
		h = y2-y1
		l = x1
		t = y1
	hwnd = win32gui.GetDesktopWindow()
	hwndDC = win32gui.GetWindowDC(hwnd)
	mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
	saveDC = mfcDC.CreateCompatibleDC()
	saveBitMap = win32ui.CreateBitmap()
	saveBitMap.CreateCompatibleBitmap(mfcDC, w,h)
	saveDC.SelectObject(saveBitMap)
	saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (l, t),  win32con.SRCCOPY)
	reformat(saveBitMap.GetInfo(), saveBitMap.GetBitmapBits(True), filename)
	mfcDC.DeleteDC()
	saveDC.DeleteDC()
	win32gui.ReleaseDC(hwnd, hwndDC)
	win32gui.DeleteObject(saveBitMap.GetHandle())

def mloc():
	return win32gui.GetCursorPos()

def takeandupload(argl, beep = sound):
	nurl = randstring() #the alias
	toclipboard('http://tinyurl.com/'+nurl)
	fn = 'temp'
	screenshot(fn, *argl)
	try:
		lnk = uploadimg(fn)
		redirect(lnk, nurl) #redirect it
		print 'done'
	except:
		if beep:
			winsound.Beep(2000,400)
		print 'not done'

lasttwo = []
def OnKeyboardEvent(event):
	global skey, lkey, lasttwo, ptimeout, wipe, ltime, btime
	if event.Key == skey:
		if time.time()-ltime < btime:
			return True
		argl = [None]*4
		if len(lasttwo) == 2 and time.time()-lasttwo[-1][1] < ptimeout: #no hardcode
			argl = copy.deepcopy((lasttwo[0][0][0], lasttwo[0][0][1], lasttwo[1][0][0], lasttwo[1][0][1]))
			if wipe:
				lasttwo = []
		m = threading.Thread(target = takeandupload, args = (argl,))
		m.daemon = True
		m.start()
		ltime = time.time()
	if event.Key == lkey:
		lasttwo.append((mloc(), time.time()))
		lasttwo = lasttwo[-2:]
	return True

hm = pyHook.HookManager() 
hm.KeyDown = OnKeyboardEvent 
hm.HookKeyboard() 
pythoncom.PumpMessages()
