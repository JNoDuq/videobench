from PySide2 import QtGui, QtWidgets, QtCore
from functools import partial
from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QPainter

class Ui_fenetrePrincipale(object):
    def setupUi(self, mainWindow):

        mainWindow.setObjectName("mainWindow")

        self.gridLayout = QtWidgets.QGridLayout(mainWindow)
        self.tabwidget = QtWidgets.QTabWidget()
        self.HSplitter = QtWidgets.QSplitter()
        self.gridLayout.addWidget(self.tabwidget, 0, 1, 1, 1)
        self.tabwidget.addTab(self.HSplitter, "General")

        self.widgets_and_layouts()
        self.setting_widget()
        self.add_inputs_layout()
        self.add_checkbox()
        self.add_sync_block()
        self.add_start_btn()
        self.add_reset_btn()

    def setting_widget(self):

        self.setting_vgrid = QtWidgets.QVBoxLayout()
        self.setting_vgrid_widget = QtWidgets.QWidget()
        self.setting_vgrid_widget.setLayout(self.setting_vgrid)
        self.tabwidget.addTab(self.setting_vgrid_widget, "Settings")

        self.setting_grid = QtWidgets.QGridLayout()

        self.setting_vgrid.addLayout(self.setting_grid)
        self.setting_vgrid.setAlignment(QtCore.Qt.AlignTop)

        self.deint_setting = QtWidgets.QLabel()
        #self.deint_setting.setMaximumWidth(0.06*self.size.width())
        self.deint_setting.setText("Ref Deint filter : ")
        self.deint_setting.setStyleSheet('QLabel {background-color: transparent;}')
        self.deint_setting.setAlignment(QtCore.Qt.AlignRight)
        self.deint_combobox = QtWidgets.QComboBox()
        #self.deint_combobox.setMaximumWidth(0.06*self.size.width())
        self.deint_combobox.insertItem(0, "auto")
        self.deint_combobox.insertItem(1, "yadif=0:-1:0")
        self.deint_combobox.insertItem(2, "yadif=1:-1:0")
        self.deint_combobox.insertItem(3, "null")


        self.subsampling_setting = QtWidgets.QLabel()
        self.subsampling_setting.setText("Quality subsampling : ")
        self.subsampling_setting.setStyleSheet('QLabel {background-color: transparent;}')
        self.subsampling_setting.setAlignment(QtCore.Qt.AlignRight)
        self.subsampling_combobox = QtWidgets.QComboBox()
        self.subsampling_combobox.insertItem(0, "auto")
        self.subsampling_combobox.insertItem(1, "1")
        self.subsampling_combobox.insertItem(2, "2")
        self.subsampling_combobox.insertItem(3, "3")
        self.subsampling_combobox.insertItem(4, "4")
        self.subsampling_combobox.insertItem(5, "5")
        self.subsampling_combobox.insertItem(6, "6")
        self.subsampling_combobox.insertItem(7, "7")
        self.subsampling_combobox.insertItem(8, "8")
        self.subsampling_combobox.insertItem(9, "9")
        self.subsampling_combobox.insertItem(10, "10")


        self.scale_setting = QtWidgets.QLabel()
        self.scale_setting.setText("Scale filter : ")
        self.scale_setting.setStyleSheet('QLabel {background-color: transparent;}')
        self.scale_setting.setAlignment(QtCore.Qt.AlignRight)
        self.scale_combobox = QtWidgets.QComboBox()
        self.scale_combobox.insertItem(0, "neighbor")
        self.scale_combobox.insertItem(1, "fast_bilinear")
        self.scale_combobox.insertItem(2, "bilinear")
        self.scale_combobox.insertItem(3, "bicubic")
        self.scale_combobox.insertItem(4, "experimental")
        self.scale_combobox.insertItem(5, "area")
        self.scale_combobox.insertItem(6, "bicublin")
        self.scale_combobox.insertItem(7, "gauss")
        self.scale_combobox.insertItem(8, "sinc")
        self.scale_combobox.insertItem(9, "lanczos")
        self.scale_combobox.insertItem(10, "spline")


        self.vmaf_model_setting = QtWidgets.QLabel()
        self.vmaf_model_setting.setText("VMAF Model : ")
        self.vmaf_model_setting.setStyleSheet('QLabel {background-color: transparent;}')
        self.vmaf_model_setting.setAlignment(QtCore.Qt.AlignRight)
        self.vmaf_model_combobox = QtWidgets.QComboBox()
        self.vmaf_model_combobox.insertItem(0, "auto")
        self.vmaf_model_combobox.insertItem(1, "vmaf_float_v0.6.1.pkl")
        self.vmaf_model_combobox.insertItem(2, "vmaf_float_v0.6.1.pkl:phone_model")
        self.vmaf_model_combobox.insertItem(3, "vmaf_4k_v0.6.1.pkl")


        self.loglevel_setting = QtWidgets.QLabel()
        self.loglevel_setting.setText("Loglevel : ")
        self.loglevel_setting.setStyleSheet('QLabel {background-color: transparent;}')
        self.loglevel_setting.setAlignment(QtCore.Qt.AlignRight)
        self.loglevel_combobox = QtWidgets.QComboBox()
        self.loglevel_combobox.insertItem(0, "quiet")
        self.loglevel_combobox.insertItem(1, "info")


        self.png_resolution = QtWidgets.QLabel()
        self.png_resolution.setText("PNG Resolution : ")
        self.png_resolution.setStyleSheet('QLabel {background-color: transparent;}')
        self.png_resolution.setAlignment(QtCore.Qt.AlignRight)
        self.png_resolution_hlayout = QtWidgets.QHBoxLayout()
        self.png_resolution_hlayout.setAlignment(QtCore.Qt.AlignLeft)
        self.png_width = QtWidgets.QLineEdit()
        self.png_width.setAlignment(QtCore.Qt.AlignRight)
        self.png_width.setMaximumWidth(150)
        self.png_width.setText("1280")
        self.png_ = QtWidgets.QLabel()
        self.png_.setStyleSheet('QLabel {background-color: transparent;}')
        self.png_.setAlignment(QtCore.Qt.AlignLeft)
        self.png_.setMaximumWidth(10)
        self.png_.setText(" : ")
        self.png_height = QtWidgets.QLineEdit()
        self.png_height.setAlignment(QtCore.Qt.AlignRight)
        self.png_height.setMaximumWidth(150)
        self.png_height.setText("720")
        self.png_resolution_hlayout.addWidget(self.png_width)
        self.png_resolution_hlayout.addWidget(self.png_)
        self.png_resolution_hlayout.addWidget(self.png_height)

        self.setting_grid.addWidget(self.vmaf_model_setting, 0,0,1,1)
        self.setting_grid.addWidget(self.vmaf_model_combobox, 0,1,1,1)
        self.setting_grid.addWidget(self.scale_setting, 1,0,1,1)
        self.setting_grid.addWidget(self.scale_combobox, 1,1,1,1)
        self.setting_grid.addWidget(self.deint_setting, 2,0,1,1)
        self.setting_grid.addWidget(self.deint_combobox, 2,1,1,1)
        self.setting_grid.addWidget(self.subsampling_setting, 3,0,1,1)
        self.setting_grid.addWidget(self.subsampling_combobox, 3,1,1,1)
        self.setting_grid.addWidget(self.loglevel_setting, 4,0,1,1)
        self.setting_grid.addWidget(self.loglevel_combobox, 4,1,1,1)        
        self.setting_grid.addWidget(self.png_resolution, 5,0,1,1)
        self.setting_grid.addLayout(self.png_resolution_hlayout, 5,1,1,1)


    def widgets_and_layouts(self): 

        self.inputs_column_Layout = QtWidgets.QVBoxLayout() 

        self.inputs_btn_Layout = QtWidgets.QHBoxLayout()  ########################################### Imports Butons 
        self.btn_importRef = QtWidgets.QPushButton("Import Video")
        self.btn_importRef.setMinimumSize(0.06*self.size.width() , 0.04*self.size.height())
        self.btn_importRef.setStyleSheet('QPushButton:hover {background-color: #007bff; color: #ffffff; font-size: 15px; } QPushButton {color: #007bff; border:2px solid #007bff; background-color: transparent;  border-radius: 4px;}')
        self.btn_importRef.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_importInputs = QtWidgets.QPushButton("Import Video")
        self.btn_importInputs.setMinimumSize(0.06*self.size.width() , 0.04*self.size.height())
        self.btn_importInputs.setStyleSheet('QPushButton:hover {background-color: #007bff; color: #ffffff; font-size: 15px; } QPushButton {color: #007bff; border:2px solid #007bff; background-color: transparent;  border-radius: 4px;}')
        self.btn_importInputs.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.label_or = QtWidgets.QLabel("or")
        self.label_or.setText("or")
        self.label_or.setStyleSheet('QLabel {background-color: transparent;}')

        self.import_json_btn = QtWidgets.QPushButton("Import Measurements")
        self.import_json_btn.setMinimumSize(0.06*self.size.width() , 0.04*self.size.height())
        self.import_json_btn.setStyleSheet('QPushButton:hover {background-color: #007bff; color: #ffffff; font-size: 15px; } QPushButton {color: #007bff; border:2px solid #007bff; background-color: transparent;  border-radius: 4px;}')
        self.import_json_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        self.inputs_checkbox_Layout = QtWidgets.QHBoxLayout() ####################################### CheckBox

        self.gb_ref_file = QtWidgets.QGroupBox()   ########################## Ref Checkbox
        self.gb_ref_file.setTitle("Original Video")
        self.refLayout = QtWidgets.QVBoxLayout()
        self.gb_ref_file.setLayout(self.refLayout)

        self.ref_checkbox_vlayout = QtWidgets.QVBoxLayout()
        self.ref_checkbox_vlayout.setAlignment(QtCore.Qt.AlignTop)
        self.refLayout.addLayout(self.ref_checkbox_vlayout)

        self.ref_buttons_vLayout = QtWidgets.QVBoxLayout()
        self.ref_buttons_vLayout.setAlignment(QtCore.Qt.AlignBottom)
        self.refLayout.addLayout(self.ref_buttons_vLayout)

        self.ref_buttons_hLayout = QtWidgets.QHBoxLayout()
        self.ref_buttons_hLayout.setAlignment(QtCore.Qt.AlignRight)
        self.ref_buttons_vLayout.addLayout(self.ref_buttons_hLayout)
        

        
        self.gb_input_files = QtWidgets.QGroupBox() ########################## Innput Checkbox
        self.gb_input_files.setTitle("Compressed Videos")
        self.inputsLayout = QtWidgets.QVBoxLayout()
        self.gb_input_files.setLayout(self.inputsLayout)

        self.inputs_checkbox_vlayout = QtWidgets.QVBoxLayout()
        self.inputs_checkbox_vlayout.setAlignment(QtCore.Qt.AlignTop)
        self.inputsLayout.addLayout(self.inputs_checkbox_vlayout)

        self.inputs_buttons_vLayout = QtWidgets.QVBoxLayout()
        self.inputs_buttons_vLayout.setAlignment(QtCore.Qt.AlignBottom)
        self.inputsLayout.addLayout(self.inputs_buttons_vLayout)

        self.inputs_buttons_hLayout = QtWidgets.QHBoxLayout()
        self.inputs_buttons_hLayout.setAlignment(QtCore.Qt.AlignRight)
        self.inputs_buttons_vLayout.addLayout(self.inputs_buttons_hLayout)



        self.txtedit_Layout = QtWidgets.QHBoxLayout() ############################################### txt box
        self.ref_txt = QtWidgets.QTextEdit()
        self.ref_txt.setReadOnly(True)
        self.input_txt = QtWidgets.QTextEdit()
        self.input_txt.setReadOnly(True)


        self.syncLayout = QtWidgets.QHBoxLayout() ################################################### Sync block
        self.label_sync = QtWidgets.QLabel("Sync Time : ") 
        self.label_sync.setText("Sync Time (second) : ")
        self.label_sync.setStyleSheet('QLabel {background-color: transparent;}')
        self.label_sync.setAlignment(QtCore.Qt.AlignRight)
        self.label_sync.setMaximumWidth(150)
        self.le_sync = QtWidgets.QLineEdit()
        self.le_sync.setMaximumWidth(50)
        self.le_sync.setText("0")
        self.label_sw = QtWidgets.QLabel("Sync Windows : ")
        self.label_sw.setText("Sync Windows (second) : ")
        self.label_sw.setStyleSheet('QLabel {background-color: transparent;}')
        self.label_sw.setAlignment(QtCore.Qt.AlignRight)
        self.label_sw.setMaximumWidth(175)
        self.le_sw = QtWidgets.QLineEdit()
        self.le_sw.setMaximumWidth(50)
        self.le_sw.setText("0")
        self.syncGroupBox = QtWidgets.QGroupBox()
        self.syncGroupBox.setMaximumHeight(75)
        self.syncGroupBox.setTitle("Synchronize ref. and tests files ")
        self.syncGroupBox.setStyleSheet('QGroupBox {background-color: transparent;}')


        self.startLayout = QtWidgets.QHBoxLayout() ################################################# Start and reset

        self.btn_start = QtWidgets.QPushButton("Start")
        self.btn_start.setStyleSheet('QPushButton:hover {background-color: #28a745; color: #ffffff; font-size: 15px; } QPushButton {color: #28a745; border:2px solid #28a745; background-color: transparent;  border-radius: 4px;}')
        self.btn_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_start.setMinimumSize(0.04*self.size.width() , 0.04*self.size.height())
        

        self.btn_reset = QtWidgets.QPushButton("Reset")
        self.btn_reset.setStyleSheet('QPushButton:hover {background-color: #dc3545; color: #ffffff; font-size: 15px; } QPushButton {color: #dc3545; border:2px solid #dc3545; background-color: transparent;  border-radius: 4px;}')
        self.btn_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_reset.setMinimumSize(0.04*self.size.width() , 0.04*self.size.height())

        self.btn_export_png = QtWidgets.QPushButton("Export PNG")
        self.btn_export_png.setStyleSheet('QPushButton:hover {background-color: #007bff; color: #ffffff; font-size: 15px; } QPushButton {color: #007bff; border:2px solid #007bff; background-color: transparent;  border-radius: 4px;}')
        self.btn_export_png.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_export_png.setMinimumSize(0.04*self.size.width() , 0.04*self.size.height())

        self.inputs_column_widget = QtWidgets.QWidget()
        self.inputs_column_widget.setLayout(self.inputs_column_Layout)

        self.inputs_column_Layout.insertLayout(3, self.startLayout)

        self.HSplitter.addWidget(self.inputs_column_widget)


        self.chartVSplitter = QtWidgets.QSplitter()    ############################################### Line Chart
        self.chartVSplitter.setOrientation(QtCore.Qt.Vertical) 

        self.chart_vmaf = self.create_chart("VMAF")
        self.chartView_vmaf = QtCharts.QChartView(self.chart_vmaf)
        self.chartView_vmaf.setRenderHint(QPainter.Antialiasing)    

        self.chart_psnr = self.create_chart("PSNR")
        self.chartView_psnr = QtCharts.QChartView(self.chart_psnr)
        self.chartView_psnr.setRenderHint(QPainter.Antialiasing)    

        self.chart_bitrate = self.create_chart("Bitrate Kbps")
        self.chartView_bitrate = QtCharts.QChartView(self.chart_bitrate)
        self.chartView_bitrate.setRenderHint(QPainter.Antialiasing)

        self.radio_time = QtWidgets.QRadioButton("Seconds")
        self.radio_frame = QtWidgets.QRadioButton("Frames")


        self.barVSplitter = QtWidgets.QSplitter() #################################################### Bar Chart
        self.barVSplitter.setOrientation(QtCore.Qt.Vertical) 

        self.barChart_vmaf = self.create_chart("VMAF")
        self.barChartView_vmaf = QtCharts.QChartView(self.barChart_vmaf)
        self.barChartView_vmaf.setRenderHint(QPainter.Antialiasing) 

        self.barChart_psnr = self.create_chart("PSNR")
        self.barChartView_psnr = QtCharts.QChartView(self.barChart_psnr)
        self.barChartView_psnr.setRenderHint(QPainter.Antialiasing) 

        self.barChart_bitrate = self.create_chart("Bitrate Kbps")
        self.barChartView_bitrate = QtCharts.QChartView(self.barChart_bitrate)
        self.barChartView_bitrate.setRenderHint(QPainter.Antialiasing)

    def create_chart(self, title): 
        chart = QtCharts.QChart()
        chart.setTitle(title)
        chart.setMinimumSize(0.25*self.size.width() , 0.25*self.size.height())
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        #chart.setTheme(QtCharts.QChart.ChartThemeLight)
        return chart

    def add_inputs_layout(self):
        self.inputs_column_Layout.insertLayout(0, self.inputs_btn_Layout)
        self.ref_buttons_hLayout.addWidget(self.btn_importRef)
        self.inputs_buttons_hLayout.addWidget(self.btn_importInputs)
        self.inputs_buttons_hLayout.addWidget(self.label_or)
        self.inputs_buttons_hLayout.addWidget(self.import_json_btn)

    def remove_inputs_layout(self):
        self.btn_importRef.setParent(None)
        self.btn_importInputs.setParent(None)
        self.import_json_btn.setParent(None)
        self.label_or.setParent(None)
        self.inputs_btn_Layout.setParent(None)

    def add_checkbox(self):
        self.inputs_column_Layout.insertLayout(1, self.inputs_checkbox_Layout)
        self.inputs_checkbox_Layout.addWidget(self.gb_ref_file)
        self.inputs_checkbox_Layout.addWidget(self.gb_input_files)

    def remove_checkbox_values(self) :
        for key, value in self.inputCheckbox_dict.items():
            value.setParent(None)

        for key, value in self.refCheckbox_dict.items():
            value.setParent(None)


    def remove_ref_checkbox_values(self) :
        for key, value in self.refCheckbox_dict.items():
            if type(value) == QtWidgets.QCheckBox:
                value.setParent(None)

    def remove_inputs_checkbox_values(self) :
        for key, value in self.inputCheckbox_dict.items():
            if type(value) == QtWidgets.QCheckBox:
                value.setParent(None)

    def add_sync_block(self):
        self.syncLayout.addWidget(self.label_sync)
        self.syncLayout.addWidget(self.le_sync)
        self.syncLayout.addWidget(self.label_sw)
        self.syncLayout.addWidget(self.le_sw)
        self.syncGroupBox.setLayout(self.syncLayout)
        self.inputs_column_Layout.insertWidget(2, self.syncGroupBox)
        self.syncLayout.setAlignment(QtCore.Qt.AlignRight)

    def remove_sync_block(self):
        self.label_sync.setParent(None)
        self.le_sync.setParent(None)
        self.label_sw.setParent(None)
        self.le_sw.setParent(None)
        self.syncGroupBox.setParent(None)

    def add_txtbox(self):
        self.inputs_column_Layout.insertLayout(2, self.txtedit_Layout)
        self.txtedit_Layout.addWidget(self.input_txt)

    def remove_txtbox(self):
        self.ref_txt.setParent(None)
        self.input_txt.setParent(None)
        self.txtedit_Layout.setParent(None)

    def add_start_btn(self):
        self.startLayout.addWidget(self.btn_start)
        self.startLayout.setAlignment(QtCore.Qt.AlignRight)

    def remove_start_btn(self):
        self.btn_start.setParent(None)

    def add_reset_btn(self):
        self.startLayout.insertWidget(0, self.btn_reset)

    def remove_reset_btn(self):
        self.btn_reset.setParent(None)

    def add_export_png_btn(self):
        self.startLayout.insertWidget(0, self.btn_export_png)

    def remove_export_png_btn(self):
        self.btn_export_png.setParent(None)

    def add_Chart(self):
        self.HSplitter.addWidget(self.chartVSplitter)
        self.chartVSplitter.addWidget(self.chartView_vmaf)
        self.chartVSplitter.addWidget(self.chartView_psnr)
        self.chartVSplitter.addWidget(self.chartView_bitrate)

    def remove_Chart(self):
        self.chartView_vmaf.setParent(None)
        self.chartView_psnr.setParent(None)
        self.chartView_bitrate.setParent(None)
        self.chartVSplitter.setParent(None)

    def add_radioLayout(self):
        self.radioLayout = QtWidgets.QHBoxLayout()
        self.radioLayout.addWidget(self.radio_time)
        self.radioLayout.addWidget(self.radio_frame)
        self.radioLayout.setAlignment(QtCore.Qt.AlignRight)
        self.radioLayout_widget = QtWidgets.QWidget()
        self.radioLayout_widget.setLayout(self.radioLayout)
        self.chartVSplitter.addWidget(self.radioLayout_widget)

    def remove_radioLayout(self):
        self.radio_time.setParent(None)
        self.radio_frame.setParent(None)
        self.radioLayout_widget.setParent(None)

    def add_BarChart(self):
        self.HSplitter.addWidget(self.barVSplitter)
        self.barVSplitter.addWidget(self.barChartView_vmaf)
        self.barVSplitter.addWidget(self.barChartView_psnr)
        self.barVSplitter.addWidget(self.barChartView_bitrate)

    def remove_BarChart(self):
        self.barChartView_vmaf.setParent(None)
        self.barChartView_psnr.setParent(None)
        self.barChartView_bitrate.setParent(None)
        self.barVSplitter.setParent(None)

