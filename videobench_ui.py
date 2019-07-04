import os
import sys
from subprocess import call
from subprocess import Popen, PIPE
import subprocess
from functools import partial
from datetime import datetime
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtCore import QPoint, Qt, QProcess
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCharts import QtCharts
from videobench_layout import Ui_fenetrePrincipale
from videobench_functions import videoFileInfos

import copy

import json
import time
import re



class VideoAnalyzer(QtWidgets.QWidget, Ui_fenetrePrincipale):
	def __init__(self, screen = None):
		super(VideoAnalyzer, self).__init__()

		self.screen = screen
		self.setWindowTitle('Video Bench')
		self.setStyleSheet("background-color:white");
		self.screen_infos()
		self.setupUi(self)
		self.Init_values()
		self.setupConnections()
		self.show()

	def screen_infos(self):
		self.size = screen.size()
		print('Screen Size: %d x %d' % (self.size.width(), self.size.height()))

	def Init_values(self):
		self.currentPath = os.path.dirname(__file__)
		self.videoAnalyzerPath ="python3 " + os.path.dirname(os.path.abspath(__file__)) + "/videobench.py"
		self.list_obj=[]
		self.jsonFilesNames = []
		self.refCheckbox_dict = {}
		self.inputCheckbox_dict = {}
		self.inputPath_list =[]
		self.ref_path = None
		self.progressbar_step = 0

	def reset_init_values(self):
		self.list_obj=[]
		self.jsonFilesNames = []
		self.refCheckbox_dict = {}
		self.inputCheckbox_dict = {}
		self.inputPath_list =[]
		self.ref_path = None
		self.input_txt.setText("")
		self.progressbar_step = 0

	def setupConnections(self):
		self.btn_importRef.clicked.connect(self.get_refFileName)
		self.btn_importInputs.clicked.connect(self.get_inputFileNames)
		self.import_json_btn.clicked.connect(self.get_jsondata_list)
		self.btn_start.clicked.connect(self.analyzing)
		self.btn_reset.clicked.connect(self.reset_all)
		self.radio_time.clicked.connect(self.switch_radio)
		self.radio_frame.clicked.connect(self.switch_radio)
		self.btn_export_png.clicked.connect(self.export_graph_png)
				
	def get_refFileName(self):

		self.ref_path = QtWidgets.QFileDialog.getOpenFileName(self, ("Open Reference File"),self.currentPath,("Video files (*.mp4 *.ts *.ismv *.mov *.mp2 *.mxf *.h264 *.h265);; All files (*.*)"))[0]
		self.create_refCheckBox()

	def create_refCheckBox(self): 

		if self.refLayout.count() != 0:
			self.remove_ref_checkbox_values()

		if self.ref_path:
			path, filename = os.path.split(self.ref_path)
			self.refCheckbox_dict[filename] = QtWidgets.QCheckBox(filename)
			self.refCheckbox_dict[filename].setObjectName(filename)
			self.refCheckbox_dict[filename].setEnabled(False)
			self.refCheckbox_dict[filename].setStyleSheet('QCheckBox {background-color: transparent;}')

			self.ref_checkbox_vlayout.insertWidget(0,self.refCheckbox_dict[filename])
			self.refCheckbox_dict[filename].clicked.connect(partial(self.add_lineSeries, self.refCheckbox_dict[filename]))

	def get_inputFileNames(self):
		list_input = QtWidgets.QFileDialog.getOpenFileNames(self, ("Open Test Files"),self.currentPath,("Video files (*.mp4 *.ts *.ismv *.mov *.mp2 *.mxf *.h264 *.h265);; All files (*.*)"))[0]

		for input_file in list_input: 
			if input_file not in self.inputPath_list:
				self.inputPath_list.append(input_file)

		self.create_inputsCheckBox()

	def get_jsondata_list(self):
		list_json = QtWidgets.QFileDialog.getOpenFileNames(self, ("Open Test Files"),self.currentPath,("Json files (*.json);; All files (*.*)"))[0]

		for json in list_json:
			if json not in self.jsonFilesNames :
				self.jsonFilesNames.append(json)

		self.create_inputsCheckBox()

	def create_inputsCheckBox(self):

		if self.inputsLayout.count() != 0:
			self.remove_inputs_checkbox_values()
		
		input_checkbox_list = self.inputPath_list + self.jsonFilesNames

		if input_checkbox_list:
			for inputPath in reversed(input_checkbox_list):
				path, filename = os.path.split(inputPath)
				self.inputCheckbox_dict[filename] = QtWidgets.QCheckBox(filename)
				self.inputs_checkbox_vlayout.insertWidget(0, self.inputCheckbox_dict[filename])
				self.inputCheckbox_dict[filename].setObjectName(filename)
				self.inputCheckbox_dict[filename].setEnabled(False)
				self.inputCheckbox_dict[filename].setStyleSheet('QCheckBox {background-color: transparent;}')
				self.inputCheckbox_dict[filename].clicked.connect(partial(self.add_lineSeries, self.inputCheckbox_dict[filename]))

	def enable_checkBox(self):

		for key, value in self.inputCheckbox_dict.items():
			value.setEnabled(True)

		for key, value in self.refCheckbox_dict.items():
			value.setEnabled(True)

	def make_json_list(self):
	
		for input_Path in self.inputPath_list :
			inputt, ext = os.path.splitext(input_Path)
			self.jsonFilesNames.append("{0}.json".format(inputt))

		if self.ref_path != None :
			reff, ext = os.path.splitext(self.ref_path)
			self.jsonRefName = "{0}.json".format(reff)

	def jsonToObject(self): ################## Open json files and create object

		for json_file in self.jsonFilesNames:
			data = json.load(open(json_file))
			obj = videoFileInfos()
			obj.__dict__ = data
			self.list_obj.append(obj)

		if self.ref_path and self.ref_path != None :
			self.ref_obj = videoFileInfos()
			data = json.load(open(self.jsonRefName))
			self.ref_obj.__dict__ = data

	def print_videoinfos(self):

		if self.ref_path and self.ref_path != None :
			if self.ref_obj.interlaced == 1 :
				interlaced = "Yes"
			else :
				interlaced = "No"
		
			ref_str = "{} : \n * Codec Name : {}\n * Resolution : {}:{}\n * Scale Filter : {}\n * Video Bitrate : {}Mbps \n * Framerate : {}\n * Interlaced : {}\n\n".format(self.ref_obj.filename, self.ref_obj.codec_name, self.ref_obj.resolution[0], self.ref_obj.resolution[1], self.ref_obj.scale_filter,  self.ref_obj.bitrate_avg, self.ref_obj.avg_frame_rate, interlaced)
			#self.ref_txt.setText(ref_str)
			self.input_txt.append("REFERENCE FILE :")
			self.input_txt.append("-----------------\n")
			self.input_txt.append(ref_str)


		self.input_txt.append("TESTS FILES :")
		self.input_txt.append("-----------------\n")
		for obj in self.list_obj:
			if obj.interlaced == 1 :
				interlaced = "Yes"
			else :
				interlaced = "No"

			try :
				vmaf_model = obj.vmaf_model.split('/')[-1]
			except:
				vmaf_model = None

			#input_str+= "{} : \n * Resolution : {}:{}\n * Video Bitrate : {}Mbps \n * Framerate : {}\n * Interlaced : {}\n * Best Sync : {}\n * Ref. File : {}\n * Ref. Deint. filter : {}\n * VMAF Model : {}\n * VMAF : {}\n * PSNR : {}\n\n".format(obj.filename, obj.resolution[0], obj.resolution[1],  obj.bitrate_avg, obj.avg_frame_rate, interlaced, obj.sync, obj.ref_file, obj.ref_deint ,vmaf_model , obj.vmaf_avg, obj.psnr_avg)
			input_str= "{} : \n * Codec Name : {}\n * Resolution : {}:{}\n * Video Bitrate : {}Mbps \n * Framerate : {}\n * Interlaced : {}\n * Best Sync : {}\n * Ref. File : {}\n * Ref. Deint. filter : {}\n * Scale filter : {}\n * VMAF Model : {}\n * VMAF : {}\n * PSNR : {}\n".format(obj.filename, obj.codec_name, obj.resolution[0], obj.resolution[1],  obj.bitrate_avg, obj.avg_frame_rate, interlaced, obj.sync, obj.ref_file, obj.ref_deint ,obj.scale_filter, vmaf_model , obj.vmaf_avg, obj.psnr_avg)
			self.input_txt.append(input_str)
		#self.input_txt.setText(input_str)

	def generate_lineseries(self):

		self.vmafls_dict = {}
		self.psnrls_dict = {}
		self.bitratels_dict = {}

		if self.ref_path and self.ref_path != None :
			self.ref_bitrate_ls = self.ref_obj.get_lineSeries_bitrate_s()
			self.ref_bitrate_frame_ls = self.ref_obj.get_lineSeries_bitrate_frame()

		for obj in self.list_obj:
			try:
				self.vmafls_dict[obj.filename] = obj.get_lineSeries_vmaf_s()
			except:
				pass

			try:
				self.psnrls_dict[obj.filename] = obj.get_lineSeries_psnr_s()
			except:
				pass

			try:
				self.bitratels_dict[obj.filename] = obj.get_lineSeries_bitrate_s()
			except:
				pass


		self.vmafls_frame_dict = {}
		self.psnrls_frame_dict = {}
		self.bitratels_frame_dict = {}

		for obj in self.list_obj:
			try:
				self.vmafls_frame_dict[obj.filename] = obj.get_lineSeries_vmaf()
			except:
				pass

			try:	
				self.psnrls_frame_dict[obj.filename] = obj.get_lineSeries_psnr()
			except:
				pass

			try:	
				self.bitratels_frame_dict[obj.filename] = obj.get_lineSeries_bitrate_frame()
			except:
				pass

	def add_lineSeries(self, input_widget):

		if self.radio_time.isChecked():
			if input_widget.checkState() == QtCore.Qt.CheckState.Checked :
				self.add_lineSeries_seconds(input_widget)
				self.add_barset_to_barSeries(input_widget)

			elif input_widget.checkState() == QtCore.Qt.CheckState.Unchecked :
				self.remove_lineSeries_seconds(input_widget)
				self.remove_barset_to_barSeries(input_widget)

		if self.radio_frame.isChecked():
			if input_widget.checkState() == QtCore.Qt.CheckState.Checked :
				self.add_lineSeries_frames(input_widget)
				self.add_barset_to_barSeries(input_widget)

			if input_widget.checkState() == QtCore.Qt.CheckState.Unchecked :
				self.remove_lineSeries_frames(input_widget)
				self.remove_barset_to_barSeries(input_widget)

	def add_lineSeries_seconds(self, input_widget):

		name, ext = input_widget.objectName().split('.')


		for obj in self.list_obj:
			if obj.name == name:

				self.axisX = QtCharts.QValueAxis()
				self.axisY = QtCharts.QValueAxis()

				
				try:
					self.chart_vmaf.addSeries(self.vmafls_dict[obj.filename])
					self.chart_vmaf.addAxis(self.axisX, QtCore.Qt.AlignBottom)
					self.chart_vmaf.addAxis(self.axisY, QtCore.Qt.AlignLeft)
					self.chart_vmaf.createDefaultAxes()
				except:
					pass

				try:	
					self.chart_psnr.addSeries(self.psnrls_dict[obj.filename])
					self.chart_psnr.addAxis(self.axisX, QtCore.Qt.AlignBottom)
					self.chart_psnr.addAxis(self.axisY, QtCore.Qt.AlignLeft)
					self.chart_psnr.createDefaultAxes()
				except:
					pass
				
				try:	
					self.chart_bitrate.addSeries(self.bitratels_dict[obj.filename])
					self.chart_bitrate.addAxis(self.axisX, QtCore.Qt.AlignBottom)
					self.chart_bitrate.addAxis(self.axisY, QtCore.Qt.AlignLeft)
					self.chart_bitrate.createDefaultAxes()
				except:
					pass
				
		if self.ref_path != None :
			if self.ref_obj.filename ==  input_widget.objectName():

				self.chart_bitrate.addSeries(self.ref_bitrate_ls)

				self.axisX = QtCharts.QValueAxis()
				self.axisY = QtCharts.QValueAxis()
				self.chart_bitrate.addAxis(self.axisX, QtCore.Qt.AlignBottom)
				self.chart_bitrate.addAxis(self.axisY, QtCore.Qt.AlignLeft)
				self.chart_bitrate.createDefaultAxes()

	def remove_lineSeries_seconds(self, input_widget):

		ls_list = self.chart_bitrate.series() ################ pas top 
		ls_name_list = []
		for ls in ls_list :
			name, ext = ls.name().split('.')
			ls_name_list.append(name) 

		name, ext = input_widget.objectName().split('.')

		for obj in self.list_obj:

			if obj.name == name and obj.name in ls_name_list:
				try:	
					self.chart_vmaf.removeSeries(self.vmafls_dict[obj.filename])
				except:
					pass

				try:
					self.chart_psnr.removeSeries(self.psnrls_dict[obj.filename])
				except:
					pass

				try:
					self.chart_bitrate.removeSeries(self.bitratels_dict[obj.filename])
				except:
					pass

		if self.ref_path != None :
			if self.ref_obj.filename ==  input_widget.objectName() and self.ref_obj.name in ls_name_list:
				self.chart_bitrate.removeSeries(self.ref_bitrate_ls)

	def add_lineSeries_frames(self, input_widget):

		name, ext = input_widget.objectName().split('.')

		for obj in self.list_obj:
			if obj.name == name:

				self.axisX_vmaf = QtCharts.QValueAxis()
				self.axisY_vmaf = QtCharts.QValueAxis()
				
				try:
					self.chart_vmaf.addSeries(self.vmafls_frame_dict[obj.filename])
					self.chart_vmaf.addAxis(self.axisX_vmaf, QtCore.Qt.AlignBottom)
					self.chart_vmaf.addAxis(self.axisY_vmaf, QtCore.Qt.AlignLeft)
					self.chart_vmaf.createDefaultAxes()
				except:
					pass
				
				try:
					self.chart_psnr.addSeries(self.psnrls_frame_dict[obj.filename])
					self.chart_psnr.addAxis(self.axisX_vmaf, QtCore.Qt.AlignBottom)
					self.chart_psnr.addAxis(self.axisY_vmaf, QtCore.Qt.AlignLeft)
					self.chart_psnr.createDefaultAxes()
				except:
					pass
				
				try:
					self.chart_bitrate.addSeries(self.bitratels_frame_dict[obj.filename])
					self.chart_bitrate.addAxis(self.axisX_vmaf, QtCore.Qt.AlignBottom)
					self.chart_bitrate.addAxis(self.axisY_vmaf, QtCore.Qt.AlignLeft)
					self.chart_bitrate.createDefaultAxes()
				except:
					pass


		if self.ref_path != None :
			if self.ref_obj.filename ==  input_widget.objectName():

				self.chart_bitrate.addSeries(self.ref_bitrate_frame_ls)

				self.axisX = QtCharts.QValueAxis()
				self.axisY = QtCharts.QValueAxis()
				self.chart_bitrate.addAxis(self.axisX, QtCore.Qt.AlignBottom)
				self.chart_bitrate.addAxis(self.axisY, QtCore.Qt.AlignLeft)
				self.chart_bitrate.createDefaultAxes()

	def remove_lineSeries_frames(self, input_widget):

		ls_list = self.chart_bitrate.series() ################ pas top 
		ls_name_list = []
		for ls in ls_list :
			name, ext = ls.name().split('.')
			ls_name_list.append(name) 

		name, ext = input_widget.objectName().split('.')

		for obj in self.list_obj:

			if obj.name == name and obj.name in ls_name_list:
				try:	
					self.chart_vmaf.removeSeries(self.vmafls_frame_dict[obj.filename])
				except:
					pass

				try:
					self.chart_psnr.removeSeries(self.psnrls_frame_dict[obj.filename])
				except:
					pass

				try:
					self.chart_bitrate.removeSeries(self.bitratels_frame_dict[obj.filename])
				except:
					pass

		if self.ref_path != None :
			if self.ref_obj.filename ==  input_widget.objectName() and self.ref_obj.name in ls_name_list:
				self.chart_bitrate.removeSeries(self.ref_bitrate_frame_ls)

	def remove_all_lineSeries(self):

		ls_list = self.chart_vmaf.series()
		for ls in ls_list:
			self.chart_vmaf.removeSeries(ls)

		ls_list = self.chart_psnr.series()
		for ls in ls_list:
			self.chart_psnr.removeSeries(ls)

		ls_list = self.chart_bitrate.series()
		for ls in ls_list:
			self.chart_bitrate.removeSeries(ls)

	def switch_radio(self):

		self.remove_all_lineSeries()
		self.generate_lineseries()

		for i in (range(self.inputs_checkbox_vlayout.count())):
			self.add_lineSeries(self.inputs_checkbox_vlayout.itemAt(i).widget())

		if self.ref_path != None :
			self.add_lineSeries(self.ref_checkbox_vlayout.itemAt(0).widget())

	def generate_barSet(self):

		self.vmafbs_dict = {}
		self.psnrbs_dict = {}
		self.bitratebs_dict = {}

		self.vmaf_barSeries = QtCharts.QBarSeries()
		self.psnr_barSeries = QtCharts.QBarSeries()
		self.bitrate_barSeries = QtCharts.QBarSeries()

		for obj in self.list_obj:


			try:
				self.vmafbs_dict[obj.filename] = QtCharts.QBarSet(obj.filename)
				self.vmafbs_dict[obj.filename].append([obj.vmaf_avg])
			except:
				pass
			
			try:
				self.psnrbs_dict[obj.filename] = QtCharts.QBarSet(obj.filename)
				self.psnrbs_dict[obj.filename].append([obj.psnr_avg])
			except:
				pass
			
			try:
				self.bitratebs_dict[obj.filename] = QtCharts.QBarSet(obj.filename)
				self.bitratebs_dict[obj.filename].append([obj.bitrate_avg])
			except:
				pass

	def add_barset_to_barSeries(self, input_widget):

		name, ext = input_widget.objectName().split('.')
		for obj in self.list_obj:
			if obj.name == name:

				try:
					self.vmaf_barSeries.append(self.vmafbs_dict[obj.filename])
				except:
					pass
				
				try:
					self.psnr_barSeries.append(self.psnrbs_dict[obj.filename])
				except:
					pass

				try:
					self.bitrate_barSeries.append(self.bitratebs_dict[obj.filename])
				except:
					pass

	def remove_barset_to_barSeries(self, input_widget):

		name, ext = input_widget.objectName().split('.')
		for obj in self.list_obj:
			if obj.name == name:
				self.vmaf_barSeries.take(self.vmafbs_dict[obj.filename])
				self.psnr_barSeries.take(self.psnrbs_dict[obj.filename])
				self.bitrate_barSeries.take(self.bitratebs_dict[obj.filename])

	def add_barSeries(self):

		self.barChart_vmaf.addSeries(self.vmaf_barSeries)
		self.barChart_psnr.addSeries(self.psnr_barSeries)
		self.barChart_bitrate.addSeries(self.bitrate_barSeries)

		self.axisX = QtCharts.QValueAxis()
		self.axisY = QtCharts.QValueAxis()

		self.barChart_vmaf.addAxis(self.axisX, QtCore.Qt.AlignBottom)
		self.barChart_vmaf.addAxis(self.axisY, QtCore.Qt.AlignLeft)
		self.barChart_vmaf.createDefaultAxes()

		self.barChart_psnr.addAxis(self.axisX, QtCore.Qt.AlignBottom)
		self.barChart_psnr.addAxis(self.axisY, QtCore.Qt.AlignLeft)
		self.barChart_psnr.createDefaultAxes()

		self.barChart_bitrate.addAxis(self.axisX, QtCore.Qt.AlignBottom)
		self.barChart_bitrate.addAxis(self.axisY, QtCore.Qt.AlignLeft)
		self.barChart_bitrate.createDefaultAxes()

	def remove_all_barSeries(self):
		
		bs_list = self.barChart_vmaf.series()
		for bs in bs_list:
			self.barChart_vmaf.removeSeries(bs)

		bs_list = self.barChart_psnr.series()
		for bs in bs_list:
			self.barChart_psnr.removeSeries(bs)

		bs_list = self.barChart_bitrate.series()
		for bs in bs_list:
			self.barChart_bitrate.removeSeries(bs)

	def analyzing(self):
		self.make_maxstepnumber()
		self.popup_windows()
		self.run_qprocess()

	def make_maxstepnumber(self):

		sw = self.le_sw.text()

		#### start step 
		self.maxstepnumber = 1		

		#### analyzing ref file step
		if self.ref_path != None : 
			self.maxstepnumber += 1


		##### analyzing test files step 
		self.maxstepnumber = self.maxstepnumber + len(self.inputPath_list)

		##### search sync step 
		if sw != "0" and sw != "" :
			self.maxstepnumber = self.maxstepnumber + len(self.inputPath_list)

		##### quality measures step 
		self.maxstepnumber = self.maxstepnumber + len(self.inputPath_list)

		##### results step
		self.maxstepnumber = self.maxstepnumber + len(self.inputPath_list)

	def popup_windows(self):

		self.Fenetre_popup = QtWidgets.QWidget()
		self.Fenetre_popup.setStyleSheet("background-color:white");
		self.Fenetre_popup.setMinimumSize(0.3*self.size.width() , 0.25*self.size.height())
		
		self.te_operation = QtWidgets.QTextEdit()
		self.te_operation.setReadOnly(True)
		
		self.progressbar = QtWidgets.QProgressBar()
		self.progressbar.setMinimum(0)
		self.progressbar.setMaximum(self.maxstepnumber)

		self.status_label = QtWidgets.QLabel()
		
		self.gridLayout = QtWidgets.QGridLayout(self.Fenetre_popup)
		self.gridLayout.addWidget(self.progressbar, 1, 0, 1, 4)
		self.gridLayout.addWidget(self.te_operation, 2, 0, 1, 4)
		self.gridLayout.addWidget(self.status_label,0, 0, 1, 4)




		self.Fenetre_popup.show()

	def run_qprocess(self):

		deint_setting = self.deint_combobox.currentText()
		subsampling_setting = self.subsampling_combobox.currentText()
		scale_setting = self.scale_combobox.currentText()
		vmaf_model_setting =  self.vmaf_model_combobox.currentText()

		self.progressbar_step = 1
		self.progressbar.setValue(self.progressbar_step)

		inputpath_list_str = "{}".format(" ".join(self.inputPath_list))
		sync = self.le_sync.text()
		sw = self.le_sw.text()

		if sync == "":
			sync = "0"

		sync = sync.replace(',','.')

		if sw == "":
			sw = "0"

		sw = sw.replace(',','.')
		#sw = round(float(sw))
		sw = float(sw)




		if not self.ref_path or self.ref_path == None  :
			cmd = ("{0} -i {1}".format(self.videoAnalyzerPath, inputpath_list_str, sync, sw))
		else:
			cmd = ("{0} -ref {1} -i {2} -sync {3} -sw {4} -deint {5} -subsampling {6} -scale {7} -vmaf_model {8}".format(self.videoAnalyzerPath, self.ref_path, inputpath_list_str, sync, sw, deint_setting, subsampling_setting, scale_setting, vmaf_model_setting))
			
		self.te_operation.append("*****************************")
		self.te_operation.append("STARTING VIDEO BENCH")
		self.te_operation.append(cmd)
		self.te_operation.append("*****************************")

		process = QtCore.QProcess()
		process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
		process.readyReadStandardOutput.connect(partial(self.dataReady, process))
		process.finished.connect(self.update_ui)
		process.start(cmd)

		self.setDisabled(True)

	def dataReady(self, p):

		def delete_last_line():
			self.te_operation.setFocus();
			QTextCursor = self.te_operation.textCursor();
			storeCursorPos = QTextCursor
			self.te_operation.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor);
			self.te_operation.moveCursor(QTextCursor.StartOfLine, QTextCursor.MoveAnchor);
			self.te_operation.moveCursor(QTextCursor.End, QTextCursor.KeepAnchor);
			self.te_operation.textCursor().removeSelectedText();
			self.te_operation.textCursor().deletePreviousChar();
			self.te_operation.setTextCursor(storeCursorPos);


		line_raw = (p.readAllStandardOutput())
		line = line_raw.data().decode('utf8')

		if "frame=" in line:
			for i in range(2):
				delete_last_line()
			self.te_operation.append(line)

		elif line[:12] == " Input PTS :":
			delete_last_line()
			self.te_operation.append(line)

		elif line == "":
			pass

		else:
			self.te_operation.append(line)

		if "*" in line :
			status = (line[line.find("*")+len("*"):line.rfind("...")])
			self.status_label.setText("<html><b>{}{}</b</html>".format(status,"..."))



		if "->" in line :
			step = line.count("->")
			self.progressbar_step += step
			self.progressbar.setValue(self.progressbar_step)

	def centered_windows(self):
		rect = self.geometry()
		windows_witdh = rect.width()
		windows_height = rect.height()
		self.move(0.05*self.size.width(), 0.05*self.size.height())

	def export_graph_png(self):
		
		self.png_path = QtWidgets.QFileDialog.getExistingDirectory()
		png_time = format(datetime.now().strftime("%d%m%y_%H%M%S_"))
		png_width = int(self.png_width.text())
		png_height = int(self.png_height.text())


		chart_dict = {
		"VMAF_chart" : self.chartView_vmaf,
		"PSNR_chart" : self.chartView_psnr,
		"Bitrate_chart" : self.chartView_bitrate,
		"VMAF_barchart" : self.barChartView_vmaf,
		"PSNR_barchart" : self.barChartView_psnr,
		"Bitrate_barchart" : self.barChartView_bitrate
		}


		for chart_name, chart in chart_dict.items():

			myPixmap = QtGui.QPixmap(png_width, png_height)
			chart.chart().setAnimationOptions(QtCharts.QChart.NoAnimation)
			rect_width = chart.geometry().width()
			rect_height = chart.geometry().height()
			chart.resize(png_width, png_height)
			chart.render(myPixmap)
			chart.resize(rect_width,rect_height)
			chart.chart().setAnimationOptions(QtCharts.QChart.AllAnimations)
			myPixmap.save(self.png_path+"/{}{}.png".format(png_time, chart_name), "PNG")


	def update_ui(self):

		self.status_label.setText("<html><b>{}</b</html>".format("Done!"))
		self.remove_inputs_layout()
		self.add_txtbox()
		self.remove_sync_block()
		self.remove_start_btn()
		self.add_Chart()
		self.add_BarChart()
		self.add_radioLayout()
		self.enable_checkBox()
		self.make_json_list()
		self.jsonToObject()
		self.print_videoinfos()
		self.generate_lineseries()
		self.generate_barSet()
		self.check_init()
		self.setEnabled(True)
		self.centered_windows()
		self.add_export_png_btn()
		


	def check_init(self):

		self.radio_time.setChecked(True)
		
		for i in (range(self.inputs_checkbox_vlayout.count())):
			if type(self.inputs_checkbox_vlayout.itemAt(i).widget()) == QtWidgets.QCheckBox :
				self.inputs_checkbox_vlayout.itemAt(i).widget().setCheckState(QtCore.Qt.CheckState.Checked)
				self.add_lineSeries(self.inputs_checkbox_vlayout.itemAt(i).widget())

		self.add_barSeries()

	def reset_all(self):
		self.remove_all_lineSeries()
		self.remove_all_barSeries()

		#self.remove_checkbox_values()
		
		try:
			self.remove_ref_checkbox_values()
		except:
			pass
		
		try:
			self.remove_inputs_checkbox_values()
		except:
			pass

		try:	
			self.remove_Chart()
			self.remove_BarChart()
		except:
			pass


		try:
			self.remove_txtbox()
		except:
			pass

		try:
			self.remove_export_png_btn()
		except:
			pass


		self.reset_init_values()

		try:
			self.add_inputs_layout()
			self.add_sync_block()
			self.add_start_btn()
		except:
			pass

		try:
			self.tabwidget.adjustSize()
			self.gb_ref_file.adjustSize()
			self.gb_input_files.adjustSize()
			self.adjustSize()
		except:
			pass

		try:
			self.remove_radioLayout()
		except:
			pass

app = QtWidgets.QApplication(sys.argv)
screen = app.primaryScreen()

nc = VideoAnalyzer(screen = screen)
sys.exit(app.exec_())
