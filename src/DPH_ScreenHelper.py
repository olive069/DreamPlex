# -*- coding: utf-8 -*-
"""
DreamPlex Plugin by DonDavici, 2012

https://github.com/DonDavici/DreamPlex

Some of the code is from other plugins:
all credits to the coders :-)

DreamPlex Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

DreamPlex Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
"""
#===============================================================================
# IMPORT
#===============================================================================
from enigma import eSize, getDesktop

from Components.config import config
from Components.ActionMap import HelpableActionMap
from Components.VideoWindow import VideoWindow
from Components.Label import Label
from Components.Label import MultiColorLabel

from Screens.Screen import Screen

from skin import parseColor

from DPH_Singleton import Singleton
from DP_ViewFactory import translateValues

from __common__ import printl2 as printl, addNewScreen, closePlugin, getLiveTv, getSkinResolution, getSkinHighlightedColor, getSkinNormalColor

#===============================================================================
#
#===============================================================================
class DPH_ScreenHelper(object):
	width = "195"
	height = "268"
	#===============================================================================
	#
	#===============================================================================
	def __init__(self, forceMiniTv=False):
		printl("", self, "S")

		self.stopLiveTvOnStartup = config.plugins.dreamplex.stopLiveTvOnStartup.value

		# we use this e.g in DP_View to use miniTv for backdrops via libiframe
		self.forceMiniTv = forceMiniTv

		if not self.stopLiveTvOnStartup or self.forceMiniTv:
			self["miniTv"] = VideoWindow(decoder=0)
			self.miniTvInUse = True
		else:
			self["miniTv"] = Label()

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def initMiniTv(self, width=None, height=None):
		"""
		the widht and height is in params files a param section on its own
		but for the views the settings located there for this reason
		we have both ways.
		"""
		printl("", self, "S")

		if not self.stopLiveTvOnStartup or self.forceMiniTv:
			if width is None or height is None:
				width, height = self.getMiniTvParams()
			desk = getDesktop(0)
			print str(self["miniTv"].instance)
			self["miniTv"].instance.setFBSize(desk.size())
			self["miniTv"].instance.resize(eSize(int(width), int(height)))
		else:
			self["miniTv"].hide()

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def getMiniTvParams(self):
		printl("", self, "S")

		width = 400
		height = 225
		printl("screenName: " + str(self.screenName), self, "D")

		if self.height is not None and self.width is not None:
			height = self.height
			width = self.width

		printl("width: " + str(width) + " - height: " + str(height), self, "D")
		printl("", self, "C")
		return int(width), int(height)

	#===============================================================================
	#
	#===============================================================================
	def initScreen(self, screenName):
		printl("", self, "S")

		tree = Singleton().getSkinParamsInstance()

		self.screenName = screenName

		for screen in tree.findall('screen'):
			name = str(screen.get('name'))

			if name == self.screenName:
				self.miniTv = translateValues(str(screen.get('miniTv')))
				if self.miniTv:
					self.width = screen.get('width')
					self.height = screen.get('height')
				else:
					self.Poster= translateValues(str(screen.get('usePoster')))
					if self.Poster:
						self.width = screen.get('width')
						self.height = screen.get('height')

		printl("", self, "C")

#===============================================================================
#
#===============================================================================
class DPH_PlexScreen(object):

	#===============================================================================
	#
	#===============================================================================
	def __init__(self):

		self.skinResolution = getSkinResolution()

	#===============================================================================
	#
	#===============================================================================
	def setColorFunctionIcons(self):
		# first we set the pics for buttons
		self["btn_red"].instance.setPixmapFromFile(self.guiElements["key_red"])
		self["btn_green"].instance.setPixmapFromFile(self.guiElements["key_green"])
		self["btn_yellow"].instance.setPixmapFromFile(self.guiElements["key_yellow"])
		self["btn_blue"].instance.setPixmapFromFile(self.guiElements["key_blue"])

#===============================================================================
#
#===============================================================================
class DPH_MultiColorFunctions(object):

	#===============================================================================
	#
	#===============================================================================
	def __init__(self):
		printl("", self, "S")

		self.colorFunctionContainer = {}
		self.colorFunctionContainer["red"] = {}
		self.colorFunctionContainer["green"] = {}
		self.colorFunctionContainer["yellow"] = {}
		self.colorFunctionContainer["blue"] = {}

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def setColorFunction(self, color, level, functionList):
		#printl("", self, "S")

		self.colorFunctionContainer[color][level] = functionList

		#printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def getColorFunction(self, color, level):
		printl("", self, "S")

		# we put this into try because if there is no function registered it will come a gs
		try:
			return self.colorFunctionContainer[color][level][1]
		except:
			return False

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def alterColorFunctionNames(self, level):
		printl("", self, "S")
		colorList = ["red", "green", "yellow", "blue"]

		for color in colorList:
			functionList = self.colorFunctionContainer[color][level]

			if functionList is not None:
				# if it is not already visible we change this now
				if self["btn_"+ color + "Text"].getVisible() == 0:
					self["btn_"+ color + "Text"].show()
					self["btn_"+ color].show()

				self["btn_"+ color + "Text"].setText(self.colorFunctionContainer[color][level][0])
			else:
				if self["btn_"+ color + "Text"].getVisible() == 1:
					self["btn_"+ color + "Text"].hide()
					self["btn_"+ color].hide()

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def setMultiLevelElements(self, levels):
		printl("", self, "S")
		self.levels = levels

		highlighted = parseColor(getSkinHighlightedColor())
		normal = parseColor(getSkinNormalColor())

		for i in range(1,int(levels)+1):
			self["L"+str(i)] = MultiColorLabel()
			self["L"+str(i)].foreColors = [highlighted, normal]
			self["L"+str(i)].setText(str(i))

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def setLevelActive(self, currentLevel):
		printl("", self, "S")

		self.currentFunctionLevel = currentLevel
		printl("currentFunctionLevel: " + str(self.currentFunctionLevel), self, "D")

		for i in range(1,int(self.levels)+1):
			if int(self.currentFunctionLevel) == int(i):
				self["L" + str(i)].setForegroundColorNum(0)
			else:
				self["L" + str(i)].setForegroundColorNum(1)

		printl("", self, "C")


#===============================================================================
#
#===============================================================================
class DPH_Screen(Screen):

	#===============================================================================
	#
	#===============================================================================
	def __init__(self, session):
		printl("", self, "S")

		Screen.__init__(self, session)

		self["globalActions"] = HelpableActionMap(self, "DP_PluginCloser",
			{
			    "stop":    (self.closePlugin, ""),
			}, -2)

		self.onLayoutFinish.append(self.addNewScreen)

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def addNewScreen(self):
		printl("", self, "S")

		addNewScreen(self)

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def closePlugin(self):
		printl("", self, "S")

		if config.plugins.dreamplex.stopLiveTvOnStartup.value:
			printl("restoring liveTv", self, "D")
			self.session.nav.playService(getLiveTv())

		closePlugin()

		printl("", self, "C")
