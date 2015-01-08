import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import Property
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from database import dbClass
from kivy.uix.label import Label

search_color = 'test'
search_label = 'test'
search_size = 'test'

class InventoryRoot(ScreenManager):
	pass

class PasswordScreen(Screen):
        def reset(self):
                self.ids.login.text = ''
                self.ids.password.text = ''

        def password(self,name,password):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
                sql = "SELECT * FROM passwd WHERE name = ? AND password = ?"
                cursor.execute(sql,(name,password))
                login = cursor.fetchone()
                if login:
                        return 'home'
                else:
                        content = Button(text='Close')
                        popup = Popup(title='Incorrect Login',content=content,size_hint=(None,None),size=(200, 100))
                        content.bind(on_press=popup.dismiss)
                        popup.open()
                        self.reset()
                        return 'password'

class HomeScreen(Screen):
	pass

class PasswordMaintenance(Screen):
        def reset(self):
                self.ids.name.text = "" 
                self.ids.name.hint_text = "Enter Name" 
                self.ids.password.text = "" 
                self.ids.password.hint_text = "Enter Password" 

        def add(self,name,password):
                bsdb = sqlite3.connect('backstockdb')
                cursor = bsdb.cursor()
                if name and password:
                    sql = "SELECT * FROM passwd WHERE name = ? AND password = ?"
                    cursor.execute(sql,(name,password))
                    test = cursor.fetchone()
                    if test:
                        if test[0] == name:
                                content = Button(text='Close')
                                popup = Popup(title='Incorrect Login',content=content,size_hint=(None,None),size=(200, 100))
                                content.bind(on_press=popup.dismiss)
                                popup.open()
                                bsdb.close()
                                self.reset()
                    else:
                        cursor.execute('''INSERT INTO passwd(name,password)VALUES(?,?)''',(name,password))
                        bsdb.commit()
                        self.reset()
                else:
                    content = Button(text='Close')
                    popup = Popup(title='Both fields required',content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_press=popup.dismiss)
                    popup.open()
                    bsdb.close()
                    self.reset()

class EditPassword(Screen):
#	def security(self):
#		bsdb = sqlite3.connect('backstockdb')
#		cursor = bsdb.cursor()
#		sql = "SELECT value FROM miscFields WHERE param = 'toteColor'"
#		
#		#Create Dropdown
#		dropdown = DropDown()
#		#Fill DropDown
#		for row in cursor.execute(sql):
#			btn = Button(text=row[0], size_hint_y = None, height=44)
#			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
#			dropdown.add_widget(btn)
#		mainbutton = self.ids.toteColor
#		mainbutton.bind(on_release=dropdown.open)
#		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

    
class FindTote(Screen):
	#Reset Find Tote Fields
	def reset(self):
		self.ids.toteColor.text = 'Select Tote Color'
		self.ids.toteLabel.text = ""
		self.ids.toteLabel.hint_text = 'Select Tote Label'
		self.ids.toteSize.text = 'Select Tote Size'
	#Search Button Functionality
	def search(self,toteColor,toteLabel,toteSize):
		global search_color 
		search_color = toteColor
		global search_label 
		search_label = toteLabel
		global search_size 
		search_size = toteSize
	#Fill Tote Color Dropdown and Select
	def fillToteColor(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'toteColor'"
		
		#Create Dropdown
		dropdown = DropDown()
		#Fill DropDown
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		mainbutton = self.ids.toteColor
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

#Fill Tote Color Dropdown and Select
	def fillToteSize(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'toteSize'"
		
		#Create Dropdown
		dropdown = DropDown()
		#Fill DropDown
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		mainbutton = self.ids.toteSize
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
	
class Inquire(Screen):
	def reset(self):
		self.ids.men.active = False
		self.ids.women.active = False
		self.ids.offsite.active = False
		self.ids.hung.active = False
		self.ids.fw.active = False
		self.ids.ss.active = False
		self.ids.categoryDrop.text = 'Choose Category'
		self.ids.subcatDrop.text = 'Choose Subcategory'
		self.ids.dateFrom.text = ""
		self.ids.dateFrom.hint_text = 'From mm/dd/yyyy'
		self.ids.dateTo.text = ""
		self.ids.dateTo.hint_text = 'To mm/dd/yyyy'
	#Fill Category Dropdown and Select
	def fillCategory(self):
		#Create Dropdown
		dropdown = DropDown()
		#Fill Dropdown
		for index in range(4):
			btn = Button(text='Value %d' % index, size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		#Bind new text to original button
		mainbutton = self.ids.categoryDrop
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		bsdb.close()

	#Fill Subcategory Dropdown and Select
	def fillSubcategory(self):
		#Create Dropdown
		dropdown = DropDown()
		#Fill Dropdown
		for index in range(4):
			btn = Button(text='Value %d' % index, size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		#Bind new text to original button
		mainbutton = self.ids.subcatDrop
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		bsdb.close()

class ToteManagement(Screen):
	def reset(self):
		self.ids.toteColor.text = 'Select Color'
		self.ids.toteLabel.text = ''
		self.ids.toteLabel.hint_text = 'Tote Label'
		self.ids.toteSize.text = 'Select Size'
#Fill Tote Color Dropdown and Select
	def fillToteColor(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'toteColor'"
		
		#Create Dropdown
		dropdown = DropDown()
		#Fill DropDown
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		mainbutton = self.ids.toteColor
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		bsdb.close()

	#Fill Tote Size Dropdown and Select
	def fillToteSize(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'toteSize'"

		#Create Dropdown
		dropdown = DropDown()
		#Fill Dropdown
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		#Bind new text to original button
		mainbutton = self.ids.toteSize
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		bsdb.close()

	#Add empty tote to DB
	def addTote(self,color,label,size):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
                sql = "SELECT * FROM tote WHERE toteColor = ? AND toteNumber = ? AND toteSize = ?"
                cursor.execute(sql,(color,label,size))
                test = cursor.fetchone()
                if test:
                    content = Button(text='Close')
                    popup = Popup(title='Error: Duplicate Tote',content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_press=popup.dismiss)
                    popup.open()
                    ToteManagement.reset(self)
                    bsdb.close()
                else:
                    cursor.execute('''INSERT INTO tote(toteColor,toteNumber,toteSize)VALUES(?,?,?)''',(color,label,size))
                    bsdb.commit()
                    bsdb.close()
                    content = Button(text='Close')
                    popup = Popup(title='Tote Added',content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_press=popup.dismiss)
                    popup.open()
                    ToteManagement.reset(self)

	def deleteTote(self,color,label,size):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
                sql = "SELECT * FROM tote WHERE toteColor = ? AND toteNumber = ? AND toteSize = ?"
                cursor.execute(sql,(color,label,size))
                test = cursor.fetchone()
                if test:
                    sql = "DELETE FROM tote WHERE toteColor = ? AND toteNumber = ? AND toteSize = ?"
                    cursor.execute(sql,(color,label,size))
                    bsdb.commit()
                    bsdb.close()
                    content = Button(text='Close')
                    popup = Popup(title='Tote Deleted',content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_press=popup.dismiss)
                    popup.open()
                    ToteManagement.reset(self)
                else:
                    content = Button(text='Close')
                    popup = Popup(title='Error: Tote Not Found',content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_press=popup.dismiss)
                    popup.open()
                    bsdb.close()
                    ToteManagement.reset(self)


class SettingsScreen(Screen):
	def reset(self):
		self.ids.newSize.text = ''
		self.ids.newSize.hint_text = 'New Tote Size'
		self.ids.newSeason.text = ''
		self.ids.newSeason.hint_text = 'New Season'
		self.ids.newColor.text = ''
		self.ids.newColor.hint_text = 'New Tote Color'
		self.ids.newLocation.text = ''
		self.ids.newLocation.hint_text = 'New Location'
		self.ids.newSex.text = ''
		self.ids.newSex.hint_text = 'New Sex'
		self.ids.newCat.text = ''
		self.ids.newCat.hint_text = 'New Category'
		self.ids.newSubCat.text = ''
		self.ids.newSubCat.hint_text = 'New Subcategory'

		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT * FROM req"
		cursor.execute(sql)
		test = cursor.fetchone()
                if test:   
                    if test[0] == 1:
                            self.ids.requireSex = True
                    else:
                            self.ids.requireSex = False
                    if test[1] == 1:
                            self.ids.requireSeason = True
                    else:
                            self.ids.requireSeason = False
                    if test[2] == 1:
                            self.ids.requireHung = True
                    else:
                            self.ids.requireHung = False
                    if test[3] == 1:
                            self.ids.requireSensor = True
                    else:
                            self.ids.requireSensor = False
                    if test[4] == 1:
                            self.ids.requireOffsite = True
                    else:
                            self.ids.requireOffsite = False
                    if test[5] == 1:
                            self.ids.requireOffLoc = True
                    else:
                            self.ids.requireOffLoc = False
                else:
                    sql = "INSERT INTO req(sex,season,hung,sensor,off,offLoc)VALUES(?,?,?,?,?,?)"
		    cursor.execute(sql,(0,0,0,0,0,0))
                    self.ids.requireSex = False
                    self.ids.requireSeason = False
                    self.ids.requireHung = False
                    self.ids.requireSensor = False
                    self.ids.requireOffsite = False
                    self.ids.requireOffLoc = False
		bsdb.commit()
		bsdb.close()

	def saveSettings(self,sex,season,hung,sensor,off,offLoc):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "INSERT INTO req(sex,season,hung,sensor,off,offLoc)VALUES(?,?,?,?,?,?)"
		cursor.execute(sql,(sex,season,hung,sensor,off,offLoc))
		bsdb.commit()
		bsdb.close()
		content = Button(text='Close')
		popup = Popup(title= "Settings Saved",content=content,size_hint=(None,None),size=(200, 100))
		content.bind(on_press=popup.dismiss)
		popup.open()

	#Delete Param
	def delete(self,param,value):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
                sqlSel = "SELECT value FROM miscFields WHERE param = ? AND value = ?"
                cursor.execute(sqlSel,(param,value))
                test = cursor.fetchone()
                if test:
                    sql = "DELETE FROM miscFields WHERE param = ? AND value = ?"
                    cursor.execute(sql,(param,value))
                    bsdb.commit()
                    bsdb.close()
                    content = Button(text='Close')
                    popupString = value + ' Deleted'
                    popup = Popup(title= popupString,content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_press=popup.dismiss)
                    popup.open()
                    self.reset()
                else:
                    content = Button(text='Close')
                    popupString = "No Value " + value
                    popup = Popup(title= popupString,content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_press=popup.dismiss)
                    popup.open()
                    bsdb.close()
                    self.reset()

	def add(self,param,value):
                if (not value):
                    content = Button(text='Close')
                    popup = Popup(title= 'Value Cannot Be Blank',content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_press=popup.dismiss)
                    popup.open()
                    self.reset()
                else:
                    bsdb = sqlite3.connect('backstockdb')
                    cursor = bsdb.cursor()
                    sql = "SELECT * FROM miscFields WHERE param = ? AND value = ?"
                    cursor.execute(sql,(param,value))
                    test = cursor.fetchone()
                    if test:
                        content = Button(text='Close')
                        popup = Popup(title= param + ' Already Exists',content=content,size_hint=(None,None),size=(200, 100))
                        content.bind(on_press=popup.dismiss)
                        popup.open()
                        bsdb.close()
                        self.reset()
                    else:
                        sql = "INSERT INTO miscFields(param,value)VALUES(?,?)"
                        cursor.execute(sql,(param,value))
                        bsdb.commit()
                        content = Button(text='Close')
                        popupString = value + " Added"
                        popup = Popup(title=popupString,content=content,size_hint=(None,None),size=(200,100))
                        content.bind(on_press=popup.dismiss)
                        popup.open()

class SearchResults(Screen):

	#Updates Labels in Search Results Screen
	def updateLabel(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT * FROM tote WHERE toteColor=? AND toteNumber=? AND toteSize=?"
                cursor.execute(sql,(search_color,search_label,search_size))
                test = cursor.fetchone()
                if test:
                    self.ids.totecolor.text = test[0]
                    self.ids.totelabel.text = str(test[1])
                    self.ids.totesize.text = test[2]
                    if test[3] == None:
                            date = ''
                    else:
                            date = test[3]
                    self.ids.date.text = date
                    if test[4] == None:
                            sex = 'No Sex Selected'
                    else:
                            sex = test[4]
                    self.ids.sex.text = sex
                    if test[5] == None:
                            cat = 'No Category Selected'
                    else:
                            cat = test[5]
                    self.ids.cat.text = cat
                    if test[6] == None:
                            subcat = 'No Subcategory Selected'
                    else:
                            subcat = test[6]
                    self.ids.subcat.text = subcat
                    if test[7] == None:
                            season = 'No Season Selected'
                    else:
                            season = test[7]
                    self.ids.season.text = season
                    if test[8] == 0:
                            isHung = False
                    elif test[8] == 1:
                            isHung = True	
                    else:
                            isHung = False
                    self.ids.hung.text = isHung
                    if test[9] == 0:
                            isSensor = False
                    if test[9] == 1:
                            isSensor = True
                    else:
                            isSensor = False
                    self.ids.sensor.text = isSensor
                    if test[10] == 0:
                            isOff = False
                    if test[10] == 1:
                            isOff = True
                    else:
                            isOff = False
                    self.ids.off.active = isOff
                    if test[11] == None:
                            offLoc = 'No Location Selected'
                    else:
                            offLoc = test[11]
                    self.ids.offLoc.text = offLoc
                else:
                    content = Button(text='Close')
                    popup = Popup(title='Error: Tote Not Found',content=content,size_hint=(None,None),size=(200, 100))
                    content.bind(on_release=popup.dismiss)
                    popup.open()

	#Fill Tote Sex Dropdown and Select
	def fillSex(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'sex'"

		#Create Dropdown
		dropdown = DropDown()
		#Fill Dropdown
		count = 0
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		#Bind new text to original button
		mainbutton = self.ids.sex
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		bsdb.close()

	#Fill Tote Category Dropdown and Select
	def fillCategory(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'category'"

		#Create Dropdown
		dropdown = DropDown()
		#Fill Dropdown
		count = 0
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		#Bind new text to original button
		mainbutton = self.ids.cat
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		bsdb.close()

	#Fill  Subcategory Dropdown and Select
	def fillSubcategory(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'SubCat'"

		#Create Dropdown
		dropdown = DropDown()
		#Fill Dropdown
		count = 0
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		#Bind new text to original button
		mainbutton = self.ids.subcat
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		bsdb.close()

	#Fill  Season Dropdown and Select
	def fillSeason(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'season'"

		#Create Dropdown
		dropdown = DropDown()
		#Fill Dropdown
		count = 0
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		#Bind new text to original button
		mainbutton = self.ids.season
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		bsdb.close()

	#Fill Location Dropdown and Select
	def fillLocation(self):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "SELECT value FROM miscFields WHERE param = 'location'"

		#Create Dropdown
		dropdown = DropDown()
		#Fill Dropdown
		count = 0
		for row in cursor.execute(sql):
			btn = Button(text=row[0], size_hint_y = None, height=44)
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			dropdown.add_widget(btn)
		#Bind new text to original button
		mainbutton = self.ids.offLoc
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

		bsdb.close()

	def saveTote(self,date,sex,cat,subcat,season,hung,sensor,off,offLoc,toteColor,toteNumber,toteSize):
		bsdb = sqlite3.connect('backstockdb')
		cursor = bsdb.cursor()
		sql = "UPDATE tote SET date=?, sex=?, cat=?, subcat=?, season=?, hung=?, sensor=?, off=?, offLoc=? WHERE toteColor=? AND toteNumber=? AND toteSize=?"
		inputs = "date, sex, cat, subcat,season,hung,sensor,off,offLoc,toteColor,toteNumber,toteSize"
		cursor.execute(sql, (date, sex, cat, subcat, season, hung, sensor, off, offLoc, toteColor, toteNumber, toteSize))
		bsdb.commit()
		bsdb.close()
		content = Button(text='Close')
		popup = Popup(title='Save Successfull',content=content,size_hint=(None,None),size=(200, 100))
		content.bind(on_press=popup.dismiss)
		popup.open()



	def emptyTote(self):
		self.ids.date.text = ''
		self.ids.date.hint_test = "Enter Date Filled"
		self.ids.sex.text = 'No Sex Selected'
		self.ids.cat.text = 'No Category Selected'
		self.ids.subcat.text = 'No Subcategory Selected'
		self.ids.season.text = 'No Season Selected'
		self.ids.hung.text = ''
		self.ids.hung.hint_test = "Is Tote Hung"
		self.ids.sensor.active = False
		self.ids.off.text = ''
		self.ids.off.hint_test = "Is Tote Offsite"
		self.ids.offLoc.text = 'No Location Selected'

class InquireResults(Screen):
	pass

class MyScreenManager(ScreenManager):
	pass

class InventoryManager(App):
	def build(self):
		return InventoryRoot()

if __name__ == '__main__':
	InventoryManager().run()
