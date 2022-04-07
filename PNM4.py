#!/usr/bin/env python
#############################################################################################
# Copyright 2003, Maciej "maciunio" Paczesny <maciunio (at) ask - bsi (dot) org>
#                 Lukasz "lookanio" Purgal <lookanio (at) interia (dot) pl>
#
#    This file is part of "Polish News Module".
#
#    "Polish News Module" is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    "Polish News Module" is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with "Polish News Module"; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#############################################################################################
#				Configurable options														#
#############################################################################################
# browser = "konqueror" # Obsolete from 4.00
ver = "4.21"
debug = 0 #( 0 = Off; 1 = On )
auto_add_remove_plugins = 1
slide_speed = 2 # ( only integers > 0! )
font_c = "white"
font_s = "10px"
font_s2 = "20px"
font_f = "Helvetica, sans-serif"

#############################################################################################
#				NO CHANGES BELOW (or for your responsibility)								#
#############################################################################################
import karamba
import string
import commands
import os
import sys
counter = 0
arrows = {}
x_uparrow = 0
x_downarrow = 0
x_menu_img = 0
#############################################################################################
class Test(object):
	def __init__(self,name):
		self.name = name
		self.action = {}
	def add_full(self,img):
		self.full = img
	def add_light(self,img):
		self.light = img
	def add_action(self,actions,side):
		self.action[side] = actions
#############################################################################################
class Logos_obj(object):
	def __init__(self,name):
		self.name = name
		self.path = path_news + "/" + name
		self.max_logo = self.path + "/minilogo10.png"
		self.min_logo = self.path + "/minilogo.png"
		self.action = {}
		self.visib = 0
		self.index = 0
	def add_image_max(self,widget,img):
		self.image_max = img
		karamba.attachClickArea(widget, self.image_max)
	def add_image_min(self,widget,img):
		self.image_min = img
#	def add_action(self,widget,size,img):
#		self.action[size] = karamba.attachClickArea(widget, img)
	def set_visib(self,flag):
		self.visib = flag
#############################################################################################

def initWidget(widget):
	global bg, small, handle, path_main, path_news, path_pics, path_new_plugins, dir_list, dir_name, news_area, logos_path, lighted
	global x_small, x_bg, x_handle, side, x_gap, x_reload, x_uparrow, x_downarrow, x_menu_img
	path_main = karamba.getThemePath(widget)
	path_news = path_main + "news"
	path_pics = path_main + "pics"
	path_new_plugins = path_main + "plugins"
	sys.path.append(path_main)
	fillDirs(widget)
	side = karamba.getWidgetPosition(widget)
	if side[0] == 0:
		x_gap = -2
	else:
		x_gap = 73
	news_area = karamba.createRichText(widget, "", 0)
	karamba.moveRichText(widget, news_area, x_gap, 30)
	if side[0] == 0:
		x_bg = 0
	else:
		x_bg = 75
	bg = karamba.createBackgroundImage(widget, x_bg, 19, "pics/calendar.png")
	if side[0] == 0:
		x_small = int(karamba.getImageWidth(widget, bg)) - 8
	else:
		x_small = 23
	small = karamba.createBackgroundImage(widget, x_small, 19, "pics/calendar_small.png")
	if side[0] == 0:
		x_handle = int(karamba.getImageWidth(widget, small)) + int(x_small) - 5
		handle_pic = "pics/handle_l.png"
	else:
		x_handle = 0
		handle_pic = "pics/handle_r.png"
	handle = karamba.createImage(widget, x_handle, 160, handle_pic)
	if side[0] == 0:
		x_reload = karamba.getImageWidth(widget, bg) - 45
	else:
		x_reload = 421
	x_menu_img = x_bg + 10
	x_uparrow = x_small + 5
	x_downarrow = x_small + 6
	karamba.redrawWidgetBackground(widget)
	karamba.attachClickArea(widget, handle)
	logos_(widget,"load")
	buttons(widget,"load")
	refreshAllNews(widget)
	startupScreen(widget)
	karamba.redrawWidget(widget)
	logos_path = "none"
	resolution(widget)
	lighted = {}
	print "Ready!"

def menuItemClicked(widget, menu, id):
	if id == menu_items[0]:
		Plugin(widget, "add")
	elif id == menu_items[1]:
		Plugin(widget, "del")
	else:
		pass
	pass

def widgetUpdated(widget):
	global counter
	counter += 1
	pass

def widgetClicked(widget, x, y, button):
	pass

def widgetMouseMoved(widget, x, y, button):
	global zoom, arrows
# Left panel arrows
#x 30,70
	if (x_uparrow <= x <= (x_uparrow + 40)) and (0 <= y <= 25):
		zoom = 1
		switchImages(widget, arrows['uparrow-panel'])
	elif (x_uparrow <= x <= (x_uparrow + 40)) and (403 <= y <= 428):
		zoom = 1
		switchImages(widget, arrows['downarrow-panel'])
	else:
		zoom = 0
		switchImages(widget, arrows['downarrow-panel'])
		switchImages(widget, arrows['uparrow-panel'])
# Reload button
#x 421,451
	if (x_reload <= x <= (x_reload + 30)) and (365 <= y <= 395):
		zoom = 1
		switchImages(widget, arrows['reload'])
	else:
		zoom = 0
		switchImages(widget, arrows['reload'])
# Zooming logos
	for key,val in meters.items():
		if logos[string.split(val['arr'],"_")[1]].visib == 1:
			if (val['y'] <= y <= (val['y']+46)) and (val['x'] <= x <= (val['x']+40)):
				zoom = 1
				zoomImages(widget, logos[string.split(val['arr'],"_")[1]])
			else:
				zoom = 0
				zoomImages(widget, logos[string.split(val['arr'],"_")[1]])
# Apply changes
	karamba.redrawWidget(widget)
	pass

def resolution(widget):
# Autodetect the resolution, thanks to Adam Geitgey ( and me for modifications )!
	global resX, resY
	havexwi = os.system("which xwininfo 2>&1 > /dev/null")
	if (havexwi == 0):
		pass
	else:
		if debug == 1:
			print "\nCan't find xwininfo in your path."
		else:
			pass
	fp = os.popen("xwininfo -root -stats")
	output = fp.read()
	output = output.splitlines()
	i = 0
	for x in output:
		param = x.split()
		if (len(param) > 1):
			if param[0].find("Width:") != -1:
				if debug == 1:
					print "Width: ", param[1]
				resX = int(param[1])
			if param[0].find("Height:") != -1:
				if debug == 1:
					print "Height: ", param[1]
				resY = int(param[1])
	pass

def movePanel(widget):
	global resX, resY
	window_pos = karamba.getWidgetPosition(widget)
	i = window_pos[0]
	if debug == 1:
		print "window_pos[0]: ", window_pos[0]
		print "window_pos[1]: ", window_pos[1]
		print "resX: ", resX-27
	else:
		pass
	if side[0] == 0:
		if i == 0:
			if debug == 1:
				print "L <="
			else:
				pass
			# 0 - 465 + 27
			while i >= (-438):
				karamba.moveWidget(widget, i, window_pos[1])
				i -= slide_speed
		elif i == (-438):
			if debug == 1:
				print "L >="
			else:
				pass
			while i <= 0:
				karamba.moveWidget(widget, i, window_pos[1])
				i += slide_speed
	else:
		if i == (resX-465):
			if debug == 1:
				print "R >="
			else:
				pass
			while i <= (resX-27):
				karamba.moveWidget(widget, i, window_pos[1])
				i += slide_speed
		elif i == (resX-27):
			if debug == 1:
				print "R <="
			else:
				pass
			while i >= (resX-465):
				karamba.moveWidget(widget, i, window_pos[1])
				i -= slide_speed
	pass

def meterClicked(widget, meter, button):
	global news_area, arrows, meters, logos_path, logos_dir_name, menu
	if button == 1:
		if meter == handle:
			movePanel(widget)
		if meter == arrows['uparrow-panel'].light:
			scrollLogos(widget, "up")
		if meter == arrows['downarrow-panel'].light:
			scrollLogos(widget, "down")
		if meter == arrows['reload'].light:
			if logos_path != "none":
				refreshOneNews(widget,logos_path,logos_dir_name)
		if (meter == menu_img) and (auto_add_remove_plugins == 1):
			karamba.popupMenu(widget, menu, x_menu_img+30, 365)
#			karamba.popupMenu(widget, menu, (x_bg+40), 365)
		url = string.split(str(meter), " ")
		if url[0] == "go":
#			karamba.execute(browser + " '%s' &" %(url[1]))
			karamba.execute("kfmclient openURL '" + url[1] +"' &")
		for key,val in meters.items():
			if meter == key:
				if debug == 1:
					print meters[key]
# 73
				karamba.moveRichText(widget, news_area, x_gap, 30)
				x = 1
				logos_path = path_news + "/" + val["arr"]
				logos_dir_name = string.split(val["arr"], "_")[1]
				text = """<table border="0" cellpadding"0" cellspacing="0">\n"""
				text += """<tr><td><a href=\"#go http://""" + string.split(val["arr"],"_")[1] + """\"><img src=\"""" + logos_path + """/logo.png\"></a></td></tr>\n"""
				news_arr = string.split(commands.getoutput("cat " + logos_path + "/newstemp"), "\n")
				while x < (len(news_arr)):
					text += """<tr><td>"""
					text += """<font face=\"""" + font_f + """\" size=""" + font_s + """ color=""" + font_c + """>\n"""
					text += """&nbsp;<a href=\""""
					text += """#go """ + (news_arr[x])
					text += """\">""" + news_arr[x-1] + """</a>\n"""
					text += """</font>\n"""
					text += """</td></tr>\n"""
					x += 2
				text += """</table>\n"""
				news_area = karamba.changeRichText(widget, news_area, text.decode('iso-8859-2'))
				karamba.setRichTextWidth(widget, news_area, 355)
				karamba.redrawWidget(widget)
	pass

def scrollLogos(widget, direction):
	global logos, first, last, meters
	temp = {}
	if (len(logos) > 8):
		if (direction == "up") and (logos[first].index > 0):
			logos[last].visib = 0
			karamba.hideImage(widget, logos[last].image_min)
			first = dir_list[logos[first].index-1]
			last = dir_list[logos[last].index-1]
			for key,val in logos.items():
				x = int(meters[val.image_min]["x"])
				y = int(meters[val.image_min]["y"]) + 46
				karamba.moveImage(widget, val.image_min, x, y)
				karamba.moveImage(widget, val.image_max, x-5, y-5)
				meters[val.image_min]["x"] = x
				meters[val.image_min]["y"] = y
				meters[val.image_max]["x"] = x
				meters[val.image_max]["y"] = y
			logos[first].visib = 1
			karamba.showImage(widget, logos[first].image_min)
		elif (direction == "down") and (logos[last].index < len(dir_list)-1):
			logos[first].visib = 0
			karamba.hideImage(widget, logos[first].image_min)
			first = dir_list[logos[first].index+1]
			last = dir_list[logos[last].index+1]
			for key,val in logos.items():
				x = int(meters[val.image_min]["x"])
				y = int(meters[val.image_min]["y"]) - 46
				karamba.moveImage(widget, val.image_min, x, y)
				karamba.moveImage(widget, val.image_max, x-5, y-5)
				meters[val.image_min]["x"] = x
				meters[val.image_min]["y"] = y
				meters[val.image_max]["x"] = x
				meters[val.image_max]["y"] = y
			logos[last].visib = 1
			karamba.showImage(widget, logos[last].image_min)
		else:
			if debug == 1:
				print "Unable to scroll: Last or First plugin reached!"
			else:
				pass
	else:
		if debug == 1:
			print "Not enough plugins to scroll: ", len(logos)
		else:
			pass
	pass

def zoomImages(widget, obj):
	global zoom
	if zoom == 1:
		karamba.hideImage(widget,obj.image_min)
		karamba.showImage(widget,obj.image_max)
	else:
		karamba.hideImage(widget,obj.image_max)
		karamba.showImage(widget,obj.image_min)
	pass

def switchImages(widget, img):
	global zoom
	if zoom == 1:
		karamba.hideImage(widget,img.full)
		karamba.showImage(widget,img.light)
	else:
		karamba.hideImage(widget,img.light)
		karamba.showImage(widget,img.full)
	pass

def refreshAllNews(widget):
	global news_area
	for k,v in dir_name.items():
		if debug == 1:
			print dir_name[k]
		else:
			pass
		os.system("echo 'Still downloading...\nhttp://" + (string.split(dir_name[k], "_")[1]) + "' > " + path_news + "/" + dir_name[k] + "/newstemp")
		loading = """<div style=\"color:red;font-face:Arial;size:""" + font_s2 + """;\">&nbsp;&nbsp;Now loading:</div>"""
		loading += """<div style=\"color:yellow;font-face:Arial;size:""" + font_s2 + """;\">&nbsp;&nbsp;""" + dir_name[k] + """</div>\n"""
		news_area = karamba.changeRichText(widget, news_area, loading)
		karamba.setRichTextWidth(widget, news_area, 155)
		karamba.redrawWidget(widget)
		os.system(path_news + "/" + dir_name[k] + "/getNews &")
	pass

def refreshOneNews(widget,path,name):
	os.system("echo \"Still downloading...\n http://" + name + "\" > " + path + "/newstemp")
	loading = karamba.createRichText(widget, "", 0)
	karamba.moveRichText(widget, loading, (x_gap + 8), 360)
	text = """<div align="right"><font size="-1" color="Yellow">Loading... """ + name + """</font></div>"""
	loading = karamba.changeRichText(widget, loading, text)
	karamba.redrawWidget(widget)
	os.system(path + "/getNews &")
	karamba.deleteRichText(widget,loading)
	if debug == 1:
		print "Reloaded: ", name
	else:
		pass
	pass

def startupScreen(widget):
	global news_area
#78
	karamba.moveRichText(widget, news_area, x_gap+5, 120)
	startup = """<div align="center"><font color="yellow" face="Helvetica,sans-serif">Polish News Module<br>ver. """+ver+"""</font></div><br>"""
	startup += """<div align="center">&nbsp;&nbsp;<img src=""" + path_pics + """/pnm.png></div>"""
	news_area = karamba.changeRichText(widget, news_area, startup)
	karamba.setRichTextWidth(widget, news_area, 355)
	pass

def buttons(widget,action):
	global arrows, menu_img, menu, menu_items, x_menu_img, auto_add_remove_plugins
	if action == "load":
		arrows = {}
#421
		arrows['reload'] = Test('reload')
		arrows['reload'].add_full(karamba.createImage(widget, x_reload, 365, path_pics + "/reload.png"))
		arrows['reload'].add_light(karamba.createImage(widget, x_reload, 365, path_pics + "/reloadlight.png"))
		arrows['reload'].add_action(karamba.attachClickArea(widget, arrows['reload'].full),'full')
		arrows['reload'].add_action(karamba.attachClickArea(widget, arrows['reload'].light),'light')
		if auto_add_remove_plugins == 1:
			menu_img = karamba.createImage(widget, x_menu_img, 365, path_pics + "/configure.png")
			karamba.attachClickArea(widget, menu_img)
			menu = karamba.createMenu(widget)
			menu_items = {}
			menu_items[0] = karamba.addMenuItem(widget, menu, "Add new plugin", "")
			menu_items[1] = karamba.addMenuItem(widget, menu, "Delete plugin", "")
			if debug == 1:
				print "You have choosen to have auto_add_remove_plugins possible.\n"
		else:
			if debug == 1:
				print "You have choosen not to have auto_add_remove_plugins possible.\n"
#29
		arrows['uparrow-panel'] = Test('uparrow-panel')
		arrows['uparrow-panel'].add_full(karamba.createImage(widget, x_uparrow, 0, path_pics + "/uparrow-panel.png"))
		arrows['uparrow-panel'].add_light(karamba.createImage(widget, x_uparrow, 0, path_pics + "/uparrow-panel_light.png"))
		arrows['uparrow-panel'].add_action(karamba.attachClickArea(widget, arrows['uparrow-panel'].full),'full')
		arrows['uparrow-panel'].add_action(karamba.attachClickArea(widget, arrows['uparrow-panel'].light),'light')
#29
		arrows['downarrow-panel'] = Test('downarrow-panel')
		arrows['downarrow-panel'].add_full(karamba.createImage(widget, x_downarrow, 403, path_pics + "/downarrow-panel.png"))
		arrows['downarrow-panel'].add_light(karamba.createImage(widget, x_downarrow, 403, path_pics + "/downarrow-panel_light.png"))
		arrows['downarrow-panel'].add_action(karamba.attachClickArea(widget, arrows['downarrow-panel'].full),'full')
		arrows['downarrow-panel'].add_action(karamba.attachClickArea(widget, arrows['downarrow-panel'].light),'light')
		for k, v in arrows.items():
			karamba.hideImage(widget, v.light)
		if debug == 1:
			print "Loaded Button Table"
	pass

def logos_(widget,action):
	global logos, meters, first, last
	meters = {}
	if action == "load":
		logos = {}
		y = 31 #x = 30
		x = x_small + 6
		for k, v in dir_list.items():
			logos[v] = Logos_obj(dir_name[k])
			logos[v].add_image_min(widget, karamba.createImage(widget, x, y, str(logos[v].min_logo)))
			logos[v].add_image_max(widget, karamba.createImage(widget, (x-5), (y-5), str(logos[v].max_logo)))
			logos[v].index = k
			if k == 0:
				first = v
			elif k == 7:
				last = v
			else:
				pass
			if k < 8:
				logos[v].visib = 1
			else:
				logos[v].visib = 0
			if logos[v].visib == 0:
				karamba.hideImage(widget, logos[v].image_min)
			meters[logos[v].image_min] = {"arr":logos[v].name,"size":"min","x":x,"y":y}
			meters[logos[v].image_max] = {"arr":logos[v].name,"size":"max","x":x,"y":y}
			karamba.hideImage(widget, logos[v].image_max)
			y += karamba.getImageHeight(widget, logos[v].image_min)
	elif action == "unload":
		for k, v in logos.items():
			karamba.hideImage(widget, v.image_min) # ???
			karamba.hideImage(widget, v.image_max) # ???
			karamba.deleteImage(widget, v.image_min)
			karamba.deleteImage(widget, v.image_max)
			v = {}
	else:
		pass
	pass

def fillDirs(widget):
	global dir_list, dir_name
	temp_news = string.split(commands.getoutput("ls " + path_news), "\n")
	dir_list = {}
	dir_name = {}
	for q in xrange (len(temp_news)):
		tmp_news = string.split(temp_news[q], "_")
		dir_list[q] = tmp_news[1]
		dir_name[q] = temp_news[q]
	pass

def Plugin(widget, action):
	if action == "del":
		temp = string.split(commands.getoutput("ls " + path_news), "\n")
		plugin_list = ""
		for q in xrange (len(temp)):
			plugin_list += " " + temp[q] + " " + temp[q]
		if (len(temp) == 1) and (temp[0] == ""):
			os.popen("kdialog --msgbox 'No more plugins to delete'")
		else:
			test = commands.getstatusoutput("kdialog --menu 'Select a plugin to DELETE'" + plugin_list)
			if test[0] == 0:
				status = commands.getstatusoutput("rm -d -f -r " + path_news + "/" + string.split(test[1],"\n")[1])
				logos_(widget,"unload")
				fillDirs(widget)
				logos_(widget,"load")
				if status[0] != 0:
					if debug == 1:
						print "An error occured during removal ",test[1]," !"
					else:
						pass
				else:
					if debug == 1:
						print "Succesfully removed plugin ",test[1]
					else:
						pass
			else:
				if debug == 1:
					if test[0] == 256:
						print "You pressed CANCEL button. Exit status = ",test[0]
					elif test[0] != 256 or test[0] != 0:
						print "An error occured. Exit status = ",test[0]
					else:
						pass
				else:
					pass
	elif action == "add":
		temp = string.split(commands.getoutput("ls " + path_new_plugins), "\n")
		plugin_list = ""
		for q in xrange (len(temp)):
			tmp = string.split(temp[q], ".tg")
			plugin_list += " " + tmp[0] + ".tgz" + " " + tmp[0]
		if (len(temp) == 1) and (temp[0] == ""):
			print temp[0]
			os.popen("kdialog --msgbox 'No files in plugins directory'")
		else:
			test = commands.getstatusoutput("kdialog --menu 'Select a plugin to INSTALL'" + plugin_list)
			if test[0] == 0:
				status = commands.getstatusoutput("tar -xzf " + path_new_plugins + "/" + string.split(test[1],"\n")[1] + " -C " + path_news + "/")
				plugin_file = string.split(string.split(test[1],"\n")[1],".tg")
				refreshOneNews(widget, path_news + "/" + plugin_file[0], string.split(plugin_file[0],"_")[1])
				logos_(widget,"unload")
				fillDirs(widget)
				logos_(widget,"load")
				if status[0] != 0:
					if debug == 1:
						print "An error occured during unpacking ",test[1]," !"
					else:
						pass
				else:
					if debug == 1:
						print "Succesfully installed plugin ",test[1]
					else:
						pass
			else:
				if debug == 1:
					if test[0] == 256:
						print "You pressed CANCEL button. Exit status = ",test[0]
					elif test[0] != 256 or test[0] != 0:
						print "An error occured. Exit status = ",test[0]
					else:
						pass
				else:
					pass
	else:
		pass
	pass

print "PNM "+ver+" theme loaded."
