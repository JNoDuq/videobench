import os
from subprocess import call
import subprocess
import json
import operator

from PySide2 import QtGui, QtWidgets, QtCore     ############# If you are not using the GUI , you can remove this block of import
from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCharts import QtCharts


container_tmp_path ="/home/shared-vmaf/"
tmp_path = "/tmp/videobench/"
docker_cmd = "docker container run --rm  -v {}:{} docker-videobench".format(tmp_path, container_tmp_path)

class videoFileInfos(object):
	def __init__(self,
		filename = None,
		name = None,
		path = None,
		r_frame_rate = None,
		avg_frame_rate = None,
		resolution = None,
		vmaf = None,
		vmaf_avg = None,
		vmaf_model = "auto",
		psnr = None,
		psnr_avg = None,
		ffpsnr = None,
		ffpsnr_avg = None,
		bitrate_avg = None,
		pkt_size = None,
		codec_name = None,
		interlaced = None,
		sync = 0,
		groupe = 0,
		ref_file = None,
		ref_deint = "null",
		scale_filter = "neighbor",
		n_subsample = 1,
		frame_size = None):

		self.filename = filename
		self.name = name
		self.path = path
		self.resolution = resolution
		self.r_frame_rate = r_frame_rate
		self.avg_frame_rate = avg_frame_rate
		self.vmaf = vmaf
		self.vmaf_avg = vmaf_avg
		self.vmaf_model = vmaf_model
		self.psnr = psnr
		self.psnr_avg = psnr_avg
		self.ffpsnr = ffpsnr
		self.bitrate_avg = bitrate_avg
		self.pkt_size = pkt_size
		self.codec_name = codec_name
		self.frame_size = frame_size
		self.ref_file = ref_file
		self.ref_deint = ref_deint
		self.scale_filter = scale_filter
		self.n_subsample = n_subsample
		self.interlaced = interlaced
		self.sync = sync
		self.groupe = groupe


	def get_mbps(self): 
		bitrate_mbps =[]
		try :
			start_frames = len(self.frame_size) - len(self.psnr)
		except :
			start_frames = 0

		if start_frames < 0 :
			start_frames = 0			

		frame_size_cut  =  self.frame_size[start_frames:]
		chunks = [frame_size_cut[x:x+int(self.avg_frame_rate)] for x in range(0, len(frame_size_cut), int(self.avg_frame_rate))]
		for x in range(0, len(chunks)):
			bitrate_mbps.append(sum(chunks[x])*self.avg_frame_rate/len(chunks[x]))

		return bitrate_mbps


	def get_mbps_frames(self):
		bitrate_mbps_frames =[]

		try :
			start_frames = len(self.frame_size) - len(self.psnr)
		except:
			start_frames = 0

		if start_frames < 0 :
			start_frames = 0	

		for x in range(start_frames, len(self.frame_size)):
			bitrate_mbps_frames.append(self.frame_size[x]/(1/self.avg_frame_rate))
		return bitrate_mbps_frames


	def get_vmafs(self):
		vmafs =[]
		chunks = [self.vmaf[x:x+int(self.r_frame_rate)] for x in range(0, len(self.vmaf), int(self.r_frame_rate))]
		for x in range(0, len(chunks)):
			vmafs.append(sum(chunks[x])/len(chunks[x]))
		return vmafs

	def get_psnrs(self):
		psnrs =[]
		chunks = [self.psnr[x:x+int(self.r_frame_rate)] for x in range(0, len(self.psnr), int(self.r_frame_rate))]
		for x in range(0, len(chunks)):
			psnrs.append(sum(chunks[x])/len(chunks[x]))
		return psnrs


	def get_lineSeries_vmaf(self):
		lineSeries = QtCharts.QLineSeries()
		for i in range (0,len(self.vmaf)):
			lineSeries.append(QPoint(i, self.vmaf[i]))
		lineSeries.setName(self.filename)
		return lineSeries

	def get_lineSeries_psnr(self):
		lineSeries = QtCharts.QLineSeries()
		for i in range (0,len(self.psnr)):
			lineSeries.append(QPoint(i, self.psnr[i]))
		lineSeries.setName(self.filename)
		return lineSeries

	def get_lineSeries_bitrate_frame(self):
		lineSeries = QtCharts.QLineSeries()
		mbps_frames = self.get_mbps_frames()
		for i in range (0,len(self.get_mbps_frames())):
			lineSeries.append(QPoint(i, mbps_frames[i]))
		lineSeries.setName(self.filename)
		return lineSeries

	def get_lineSeries_vmaf_s(self):
		lineSeries_vmaf = QtCharts.QLineSeries()
		vmafs = self.get_vmafs()
		for i in range (0,len(self.get_vmafs())):
			lineSeries_vmaf.append(QPoint(i, vmafs[i]))
		lineSeries_vmaf.setName(self.filename)
		return lineSeries_vmaf

	def get_lineSeries_psnr_s(self):
		lineSeries_psnr = QtCharts.QLineSeries()
		psnrs = self.get_psnrs()
		for i in range (0,len(self.get_psnrs())):
			lineSeries_psnr.append(QPoint(i, psnrs[i]))
		lineSeries_psnr.setName(self.filename)
		return lineSeries_psnr

	def get_lineSeries_bitrate_s(self):
		lineSeries_bitrate = QtCharts.QLineSeries()
		mbps = self.get_mbps()
		for i in range (0,len(self.get_mbps())):
			lineSeries_bitrate.append(QPoint(i, mbps[i]))
		lineSeries_bitrate.setName(self.filename)
		return lineSeries_bitrate

def set_reference_deint_old(ref_obj, input_obj):


	if ref_obj.interlaced == 1 and input_obj.interlaced == 0 and round(int(ref_obj.r_frame_rate)) == round(int(input_obj.r_frame_rate)*2) :
		input_obj.ref_deint = "yadif=0:-1:0"


	elif ref_obj.interlaced == 1 and input_obj.interlaced == 0 and round(int(ref_obj.r_frame_rate)*2) == round(int(input_obj.r_frame_rate)) :
		input_obj.ref_deint = "yadif=1:-1:0"

	elif ref_obj.interlaced == 1 and input_obj.interlaced == 1:
		input_obj.ref_deint = "null"


	elif ref_obj.interlaced == 0 :
		input_obj.ref_deint = "null"

def set_reference_deint(ref_obj, input_obj):


	if ref_obj.interlaced == 1 and input_obj.interlaced == 0 :

		if round(int(ref_obj.r_frame_rate)) == round(int(input_obj.r_frame_rate)*2) :
			input_obj.ref_deint = "yadif=0:-1:0"
	
		if round(int(ref_obj.r_frame_rate)) == round(int(input_obj.r_frame_rate)) :
			input_obj.ref_deint = "yadif=1:-1:0"

	elif ref_obj.interlaced == 1 and input_obj.interlaced == 1:
		input_obj.ref_deint = "null"

	elif ref_obj.interlaced == 0 :
		input_obj.ref_deint = "null"

def set_subsampling(ref_obj, input_obj):


	if ref_obj.interlaced == 0 and round(int(ref_obj.avg_frame_rate)) != round(int(input_obj.avg_frame_rate)) :
		input_obj.n_subsample = round(round(int(ref_obj.avg_frame_rate))/round(int(input_obj.avg_frame_rate)))	

	else:
		input_obj.n_subsample = 1

def set_vmaf_model(ref_obj, input_obj):


	if input_obj.vmaf_model == "auto":

		if ref_obj.resolution[0] > 1920: ############################################### VMAF Model
			input_obj.vmaf_model = '/usr/local/share/model/vmaf_4k_v0.6.1.pkl'
		else:
			input_obj.vmaf_model = '/usr/local/share/model/vmaf_v0.6.1.pkl'

	elif input_obj.vmaf_model == "vmaf_v0.6.1.pkl":
		input_obj.vmaf_model = '/usr/local/share/model/vmaf_v0.6.1.pkl'

	elif input_obj.vmaf_model == "vmaf_4k_v0.6.1.pkl":
		input_obj.vmaf_model = '/usr/local/share/model/vmaf_4k_v0.6.1.pkl'

	elif input_obj.vmaf_model == "vmaf_v0.6.1.pkl:phone_model":
		input_obj.vmaf_model = '/usr/local/share/model/vmaf_v0.6.1.pkl:phone_model=1'


def set_scaling_filter(ref_obj, input_obj):

	if input_obj.vmaf_model == "/usr/local/share/model/vmaf_v0.6.1.pkl" or input_obj.vmaf_model == "/usr/local/share/model/vmaf_v0.6.1.pkl:phone_model=1":
	
		if ref_obj.resolution[0] == 1920  and ref_obj.resolution[1] == 1080 :
			ref_obj.scale_filter = "null"
		else:
			ref_obj.scale_filter = 'scale=1920:1080:flags={}'.format(input_obj.scale_filter)

		if input_obj.resolution[0] == 1920  and input_obj.resolution[1] == 1080:
			input_obj.scale_filter = "null"
		else:
			input_obj.scale_filter = 'scale=1920:1080:flags={}'.format(input_obj.scale_filter)


	if input_obj.vmaf_model == "/usr/local/share/model/vmaf_4k_v0.6.1.pkl":

		if ref_obj.resolution[0] == 3840  and ref_obj.resolution[1] == 2160 :
			ref_obj.scale_filter = "null"
		else:
			ref_obj.scale_filter = 'scale=3840:2160:flags={}'.format(input_obj.scale_filter)

		if input_obj.resolution[0] == 3840  and input_obj.resolution[1] == 2160:
			input_obj.scale_filter = "null"
		else:
			input_obj.scale_filter = 'scale=3840:2160:flags={}'.format(input_obj.scale_filter)

def get_video_streams_info(input_file):  
	cmd = "{0} ffprobe -loglevel panic -print_format json -show_streams -select_streams v -i {1}{2}".format(docker_cmd , container_tmp_path, input_file)
	result = subprocess.check_output(cmd, shell=True)
	return json.loads(result)

def find_sync_values (ref_obj, input_obj, sync, sw):

	print("-> Search sync values for : {0}".format(input_obj.filename),flush=True)
	print("",flush=True)

	psnr_value = []
	sync_value = []

	sync_step = round( 1/ ref_obj.r_frame_rate, 5) 
	
	sync_frame_position = round(sync/sync_step)
	sync = sync_frame_position*sync_step


	sw = round(sw/sync_step)



	print (" sync_step : " + str(sync_step).strip("\n"),flush=True)

	for i in range(0, int(sw)+1):

		if sync >= 0:
			sync_str = "+{0}".format(str(sync))
		else:
			sync_str = str(sync)

		sync_value.append(sync)
		psnr = get_sync_psnr(ref_obj, input_obj, sync_str, ref_obj.resolution)
		psnr_value.append(psnr)
		print(" Input PTS : " + sync_str + " => 3s PSNR = {}".format(str(psnr)),flush=True)

		sync = round(sync+sync_step, 5)

	index, value = max(enumerate(psnr_value), key=operator.itemgetter(1))

	print(" Best Sync : "+str(sync_value[index]),flush=True)
	print(" 3s PSNR : "+str(psnr_value[index]),flush=True)
	print("",flush=True)

	return sync_value[index]

def get_sync_psnr (ref_obj, input_obj, sync_str, ref_resolution):

	cmd = ("{0} ffmpeg -y -i {1}{2} -i {1}{3} -ss {4} -t 3 -lavfi '[0]{5}[ref];[1]setpts=PTS{4}/TB[b];[b]scale={6}:{7}[c];[ref][c]psnr=stats_file=psnr_Test.log' -f null -".format(docker_cmd, container_tmp_path, ref_obj.filename, input_obj.filename, sync_str, input_obj.ref_deint, ref_resolution[0], ref_resolution[1]))		

	psnr_raw = (subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)).decode('utf-8')
	psnr_list =  psnr_raw.split(" ")
	average = [s for s in psnr_list if "average" in s]
	average_name,average_value = average[0].split(":")
	return float(average_value)

def call_frames_info(args):
	make_frames_info(*args)

def make_frames_info(input_obj): 
	cmd = ('''{0} ffprobe -i {1}{2} -loglevel fatal -show_frames -print_format json -select_streams v > {3}frames_{4}.json'''.format(docker_cmd, container_tmp_path, input_obj.filename, tmp_path, input_obj.name))
	subprocess.call(cmd, shell=True)

def call_packets_info(args):
	make_packets_info(*args)

def make_packets_info(input_obj): 
	cmd = ('''{0} ffprobe -i {1}{2} -loglevel fatal -show_packets -print_format json -select_streams v > {3}packets_{4}.json'''.format(docker_cmd, container_tmp_path, input_obj.filename, tmp_path, input_obj.name))
	subprocess.call(cmd, shell=True)

def call_quality_info(args):
    make_quality_info(*args)

def make_quality_info(ref_obj, input_obj):


	sync_time = float(input_obj.sync) ############################################# sync time 
	sync_time = round(sync_time, 2)

	if sync_time >= 0 :
		sync_time_str = "+{0}".format(str(sync_time))
	else:
		sync_time_str = str(sync_time)

	'''
	if input_obj.vmaf_model == "/usr/local/share/model/vmaf_v0.6.1.pkl" or input_obj.vmaf_model == "/usr/local/share/model/vmaf_v0.6.1.pkl:phone_model=1":
	
		if ref_obj.resolution[0] == 1920  and ref_obj.resolution[1] == 1080 :
			ref_scale_filter = "null"
			ref_obj.scale_filter = "null"
		else:
			ref_scale_filter = 'scale=1920:1080:flags={}'.format(input_obj.scale_filter)

		if input_obj.resolution[0] == 1920  and input_obj.resolution[1] == 1080:
			test_scale_filter = "null"
			input_obj.scale_filter = "null"
		else:
			test_scale_filter = 'scale=1920:1080:flags={}'.format(input_obj.scale_filter)


	if input_obj.vmaf_model == "/usr/local/share/model/vmaf_4k_v0.6.1.pkl":

		if ref_obj.resolution[0] == 3840  and ref_obj.resolution[1] == 2160 :
			ref_scale_filter = "null"
			ref_obj.scale_filter = "null"
		else:
			ref_scale_filter = 'scale=3840:2160:flags={}'.format(input_obj.scale_filter)

		if input_obj.resolution[0] == 3840  and input_obj.resolution[1] == 2160:
			test_scale_filter = "null"
			input_obj.scale_filter = "null"
		else:
			test_scale_filter = 'scale=3840:2160:flags={}'.format(input_obj.scale_filter)
	
	'''

	print("",flush=True)
	print("-> {0} ".format(input_obj.filename),flush=True)
	print(" Reference deint_filter : {1}".format(ref_obj.filename, input_obj.ref_deint),flush=True)
	print(" VMAF Model : {0}".format(input_obj.vmaf_model),flush=True)
	print(" Scale filter : {0}".format(input_obj.scale_filter),flush=True)
	print(" Quality Subsampling : {1}".format(input_obj.filename, input_obj.n_subsample),flush=True)
	print(" Calculate VMAF & PSNR (libvmaf)",flush=True)
	print("",flush=True)


	cmd = (''' {0} ffmpeg -y -loglevel quiet -stats -i {1}{2} -i {1}{3} -lavfi "[0]{10}[refdeint];[refdeint]{12}[ref];[1]setpts=PTS{4}/TB[b];[b]{13}[c];[ref][c]libvmaf='log_fmt=json:psnr=1:model_path={7}:n_subsample={8}:log_path={1}quality_{9}.json'" -f null - ''').format(docker_cmd, container_tmp_path, ref_obj.filename, input_obj.filename, sync_time_str, ref_obj.resolution[0], ref_obj.resolution[1], input_obj.vmaf_model, input_obj.n_subsample, input_obj.name, input_obj.ref_deint, input_obj.scale_filter, ref_obj.scale_filter, input_obj.scale_filter)

	
	subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
