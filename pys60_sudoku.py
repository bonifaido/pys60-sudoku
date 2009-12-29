#
#	pys60_sudoku
# A simple sudoku game for S60 based phones.
#
#	Copyright (C) 2008-2009 Nandor Istvan Kracser
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


__all__ = ["Board", "Game"]

import appuifw
from graphics import *
import key_codes
import e32
import copy # csak a sudoku tabla masolasaert
import random


class Board:
	boardlist = []
	partialboardlist = []
	
	def __init__(self):
		self.boardlist = []
		self.partialboardlist = []

	def generate(self, numFilled=(9*9)):
		# cleaning cleaning cleaning
		self.boardlist = []
		self.partialboardlist = []
		slots = []
		fillOrder = []

		random.seed()

		# setup board
		row = [0,0,0,0,0,0,0,0,0]
		for i in range(0, 9):
			self.boardlist.append(row[:])

		for j in range(0, 9):
			for i in range(0, 9):
				slots.append((i,j))

		self.search(slots, 0)
		
		while len(slots) > 0:
			i = random.randint(0, len(slots)-1)
			fillOrder.append(slots[i])
			del slots[i]

		# setup board
		for i in range(0, 9):
			self.partialboardlist.append(row[:])

		for i in range(0, numFilled):
			j = fillOrder[i]
			self.partialboardlist[j[0]][j[1]] = self.boardlist[j[0]][j[1]]

	def search(self, slots, index):
		nums = []
		fillOrder = []

		if len(slots) == index:
			return self.check()

		for i in range(1, 10):
			nums.append(i)

		while len(nums) > 0:
			i = random.randint(0, len(nums)-1)
			fillOrder.append(nums[i])
			del nums[i]

		for i in fillOrder:
			x = slots[index][0]
			y = slots[index][1]
			self.boardlist[x][y] = i
			if (self.check()):
				if self.search(slots, index+1):
					return True
			self.boardlist[x][y] = 0
		return False

	def check(self):
		for i in range(0, 9):
			if (not self.checkRow(i)) or (not self.checkCol(i)) or (not self.checkSquare(i)):
				return False
		return True
	
	def checkRow(self, row):
		found = []
		for i in range(0, 9):
			if not self.boardlist[i][row] == 0:
				if self.boardlist[i][row] in found:
					return False
				found.append(self.boardlist[i][row])
		return True

	def checkCol(self, col):
		found = []
		for j in range(0, 9):
			if not self.boardlist[col][j] == 0:
				if self.boardlist[col][j] in found:
					return False
				found.append(self.boardlist[col][j])
		return True

	def checkSquare(self, square):
		found = []
		xoffset = (3*(square % 3))
		yoffset = int(square / 3) * 3
		for j in range(0, 3):
			for i in range(0, 3):
				if not self.boardlist[xoffset+i][yoffset+j] == 0:
					if self.boardlist[xoffset+i][yoffset+j] in found:
						return False
					found.append(self.boardlist[xoffset+i][yoffset+j])
		return True

	def getList(self):
		row = [0,0,0,0,0,0,0,0,0]
		for i in range(0, 9):
			self.boardlist.append(row[:])
		return self.boardlist

	def printBoard(self):
		for j in range(0, 9):
			for i in range(0, 9):
				if self.boardlist[i][j] == 0:
					print '.',
				else:
					print self.boardlist[i][j],
			print

	def printPartialBoard(self):
		for j in range(0, 9):
			for i in range(0, 9):
				if self.partialboardlist[i][j] == 0:
					print '.',
				else:
					print self.partialboardlist[i][j],
			print

	def _checkRow(self, row):
		found = []
		for i in range(0, 9):
			if self.boardlist[i][row] == 0:
				return False
			if self.boardlist[i][row] in found:
				return False
			found.append(self.boardlist[i][row])
		return True

	def _checkCol(self, col):
		found = []
		for j in range(0, 9):
			if self.boardlist[col][j] == 0:
				return False
			if self.boardlist[col][j] in found:
				return False
			found.append(self.boardlist[col][j])
		return True

	def _checkSquare(self, square):
		found = []
		xoffset = (3*(square % 3))
		yoffset = int(square / 3) * 3
		for j in range(0, 3):
			for i in range(0, 3):
				if self.boardlist[xoffset+i][yoffset+j] == 0:
					return False
				if self.boardlist[xoffset+i][yoffset+j] in found:
					return False
				found.append(self.boardlist[xoffset+i][yoffset+j])
		return True

	def _check(self):
		self.boardlist = copy.deepcopy(self.partialboardlist)
		for i in range(0, 9):
			if (not self._checkRow(i)) or (not self._checkCol(i)) or (not self._checkSquare(i)):
				return False
		return True
		

class Game (object):

	def __init__(self):
		self.canvas = appuifw.Canvas(redraw_callback=self.redraw, event_callback=self.paint_table)
		self.img = Image.new(self.canvas.size)
		self.w_unit = self.canvas.size[0] / 9
		self.h_unit = self.canvas.size[1] / 9
		self.fontsize = 20
		self.border_color = (0,100,255)
		self.row = 0 # a keret kiindulasi pozicioja, es kesobb az aktualis pozicioja
		self.coll = 0
		self.blankcells = 51
		self.b = Board()
		self.b.generate(9*9 - self.blankcells)
		# meglegyen az eredeti peldany, az osszehasonlitasok miatt
		self.ref_list = copy.deepcopy(self.b.partialboardlist)
		appuifw.app.title = u"Sudoku"
		appuifw.app.screen = "normal"
		self.menu = [
				(u"New", self.generateboard),
				(u"Check", self.check),
				(u"Difficulty", self.change_difficulty),
				(u"About", self.about)
					]
		appuifw.app.menu = self.menu
		appuifw.app.body = self.canvas
		appuifw.app.exit_key_handler = self.quit
		self.app_lock = e32.Ao_lock()
		self.app_lock.wait()


	def paint_table(self,event=None):
		self.img.clear()

		if event:
			if event['keycode']==key_codes.EKey1 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 1
			elif event['keycode']==key_codes.EKey2 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 2
			elif event['keycode']==key_codes.EKey3 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 3
			elif event['keycode']==key_codes.EKey4 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 4
			elif event['keycode']==key_codes.EKey5 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 5
			elif event['keycode']==key_codes.EKey6 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 6
			elif event['keycode']==key_codes.EKey7 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 7
			elif event['keycode']==key_codes.EKey8 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 8
			elif event['keycode']==key_codes.EKey9 and self.ref_list[self.coll][self.row] == 0:
				self.b.partialboardlist[self.coll][self.row] = 9
			elif event['keycode']==key_codes.EKeyUpArrow:
				if (self.coll -	1) < 0:
					self.coll = 8
				else:
					self.coll -= 1
			elif event['keycode']==key_codes.EKeyDownArrow:
				if (self.coll + 1) > 8:
					self.coll = 0
				else:
					self.coll += 1
			elif event['keycode']==key_codes.EKeyLeftArrow:
				if (self.row - 1) < 0:
					self.row = 8
				else:
					self.row -= 1
			elif event['keycode']==key_codes.EKeyRightArrow:
				if (self.row + 1) > 8:
					self.row = 0
				else:
					self.row += 1
		
		# alkoto keretek felrajzolasa, 4 vastagabb keret is van
		for i in range(1,9):
			_width = 1
			if i%3 == 0:
				_width = 3
			self.img.line(((i*self.w_unit, 0), (i*self.w_unit, self.img.size[1])), width=_width, outline=(0,0,0))
			self.img.line(((0, i*self.h_unit), (self.img.size[0], i*self.h_unit)), width=_width, outline=(0,0,0))
		
		# az aktualis cella korulrajzolasa
		self.img.line(((self.row*self.w_unit,self.coll*self.h_unit),((self.row+1)*self.w_unit,self.coll*self.h_unit)), \
			width=3, outline=self.border_color) # felso vonal
		self.img.line(((self.row*self.w_unit,(self.coll+1)*self.h_unit),((self.row+1)*self.w_unit,(self.coll+1)*self.h_unit)), \
			width=3, outline=self.border_color) # also vonal
		self.img.line(((self.row*self.w_unit,self.coll*self.h_unit),(self.row*self.w_unit,(self.coll+1)*self.h_unit)), \
			width=3, outline=self.border_color) # bal vonal
		self.img.line((((self.row+1)*self.w_unit,(self.coll+1)*self.h_unit),((self.row+1)*self.w_unit,self.coll*self.h_unit)), \
			width=3, outline=self.border_color) # jobb vonal

		for i in range(0,9):
			for j in range(0,9):
				if not self.b.partialboardlist[i][j] == 0:
					_color = (0,0,0)
					if not self.ref_list[i][j] == 0:
						_color = (128,128,128)
					# font maggassagat es szelesseget is belekalkulaljuk
					self.img.text( (j*self.w_unit + self.w_unit/2 - self.fontsize/4, i*self.h_unit + self.h_unit/2 + self.fontsize/2), \
						unicode(str(self.b.partialboardlist[i][j])), \
						_color, font=(None,self.fontsize,FONT_BOLD | FONT_ANTIALIAS), )

		self.canvas.blit(self.img)
	
	# a canvas redraw_callbackje, at kell venni a parametert (redraw terulet)
	def redraw(self,param):
		self.canvas.blit(self.img)

	# menu functions
	def generateboard(self):
		self.b.generate(9*9 - self.blankcells)
		self.ref_list = copy.deepcopy(self.b.partialboardlist)
		self.paint_table()

	def check(self):
		if self.b._check():
			appuifw.note(u"Success","conf")
			if appuifw.query(u'Next game?', 'query'):
				self.generateboard()
		else:
			appuifw.note(u"Fail","error")

	def change_difficulty(self):
		self.blankcells = appuifw.query(u"How many blank cells do you want? (1-80)","number")
		while self.blankcells > 80 or self.blankcells < 1:
			self.blankcells = appuifw.query(u"Please choose between 1 and 80!.","number")
		self.generateboard()

	def about(self):
		appuifw.note(u"Visit http://github.com/bonifaido/","info")

	def quit(self):
		self.app_lock.signal()


if __name__ == '__main__':
	Game()
