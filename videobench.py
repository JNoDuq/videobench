#!/usr/local/bin/python3

from sys import argv
import sys
import argparse
import os
from shutil import copyfile
from shutil import rmtree
import json
from multiprocessing import Pool
from videobench_functions import *

tmp_path = "/tmp/videobench/"
#p = Pool(1)

def manage_ref_file(ref_file, loglevel):
		
		ref_path, filename = os.path.split(ref_file)
		copyfile(ref_file, tmp_path + filename) ################ copy ref file  to local tmp path

		ffprobe_json = get_video_streams_info(filename, loglevel) ############ get video file info 
		ref_obj = videoFileInfos()
		ref_obj.path = ref_path
		ref_obj.filename = filename
		ref_obj.name , ext = os.path.splitext(filename)

		fps_str = ffprobe_json['streams'][0]['r_frame_rate']
		num,den = fps_str.split( '/' )
		ref_obj.r_frame_rate = round((float(num)/float(den)),0)

		fps_str = ffprobe_json['streams'][0]['avg_frame_rate']
		num,den = fps_str.split( '/' )
		ref_obj.avg_frame_rate = round((float(num)/float(den)),0)

		ref_obj.codec_name = ffprobe_json['streams'][0]['codec_name']
		
		ref_obj.resolution = [ffprobe_json['streams'][0]['width'], ffprobe_json['streams'][0]['height']]

		make_packets_info(ref_obj, loglevel) ############################################################################### Bitrate from packets
		data_json = json.load(open("{0}packets_{1}.json".format(tmp_path, ref_obj.name)))
		pkt_size_list = []
		for i in range(len(data_json['packets'])):
			try:
				pkt_size_list.append(int(data_json['packets'][i]["size"])*8/1000/1000)
			except Exception:
				pass
		ref_obj.pkt_size = pkt_size_list
				
		make_frames_info(ref_obj, loglevel)
		data_json = json.load(open("{0}frames_{1}.json".format(tmp_path, ref_obj.name)))
		interlaced_frame_list = []
		ref_obj.frame_size = []
		for i in range(len(data_json['frames'])):
			try:
				interlaced_frame_list.append(int(data_json['frames'][i]["interlaced_frame"]))
				ref_obj.frame_size.append(int(data_json['frames'][i]["pkt_size"])*8/1000)
			except Exception:
				pass
		ref_obj.interlaced = round(sum(interlaced_frame_list)/len(interlaced_frame_list))
		ref_obj.bitrate_avg = round(sum(ref_obj.get_mbps())/len(ref_obj.get_mbps()),2)

		print("-> {0} ".format(ref_obj.filename),flush=True)
		print(" Bitrate  : {1} Mbps".format(ref_obj.filename, round(ref_obj.bitrate_avg/1000,2)),flush=True)
		print(" avg_framerate : {1}".format(ref_obj.filename, ref_obj.avg_frame_rate),flush=True)
		print(" interlaced : {1} ".format(ref_obj.filename, ref_obj.interlaced),flush=True)
		
		return ref_obj

def manage_input_files(all_input, loglevel):

	for input_list in all_input:
		for input_file in input_list:

			input_path, filename = os.path.split(input_file) 
			copyfile(input_file, tmp_path + filename) ################################## copy input file  to local tmp path

			ffprobe_json = get_video_streams_info(filename, loglevel) ############################ get video file info 
			input_obj = videoFileInfos()
			input_obj.filename = filename
			input_obj.path = input_path
			input_obj.name, ext = os.path.splitext(filename)

			fps_str = ffprobe_json['streams'][0]['r_frame_rate']
			num,den = fps_str.split( '/' )
			input_obj.r_frame_rate = round((float(num)/float(den)),0)

			fps_str = ffprobe_json['streams'][0]['avg_frame_rate']
			num,den = fps_str.split( '/' )
			input_obj.avg_frame_rate = round((float(num)/float(den)),0)

			input_obj.codec_name = ffprobe_json['streams'][0]['codec_name']
			
			input_obj.resolution = [ffprobe_json['streams'][0]['width'], ffprobe_json['streams'][0]['height']]

			list_input_obj.append(input_obj)

	arguments = []
	for input_obj in list_input_obj:
		#arguments.append([input_obj])
		make_packets_info(input_obj, loglevel)
		make_frames_info(input_obj, loglevel)

	#p.map(call_packets_info, arguments)
	#p.map(call_frames_info, arguments)

	for input_obj in list_input_obj:
		data_json = json.load(open("{0}packets_{1}.json".format(tmp_path, input_obj.name)))
		pkt_size_list = []
		for i in range(len(data_json['packets'])):
			try:
				pkt_size_list.append(int(data_json['packets'][i]["size"])*8/1000/1000)
			except Exception:
				pass
		input_obj.pkt_size = pkt_size_list
		
		data_json = json.load(open("{0}frames_{1}.json".format(tmp_path, input_obj.name)))
		interlaced_frame_list = []
		input_obj.frame_size = []
		for i in range(len(data_json['frames'])):
			try:
				interlaced_frame_list.append(int(data_json['frames'][i]["interlaced_frame"]))
				input_obj.frame_size.append(int(data_json['frames'][i]["pkt_size"])*8/1000)
			except Exception:
				pass
		input_obj.interlaced = round(sum(interlaced_frame_list)/len(interlaced_frame_list))
		input_obj.bitrate_avg = round(sum(input_obj.get_mbps())/len(input_obj.get_mbps()),2)


		print("-> {0} ".format(input_obj.filename),flush=True)
		print(" Bitrate : {1} Mbps".format(input_obj.filename, round(input_obj.bitrate_avg/1000,2)),flush=True)
		print(" avg_framerate : {1}".format(input_obj.filename, input_obj.avg_frame_rate),flush=True)
		print(" interlaced : {1} ".format(input_obj.filename, input_obj.interlaced),flush=True)



	return list_input_obj


if __name__ == '__main__':

	######################### declaration argument ##############
	parser = argparse.ArgumentParser()

	parser.add_argument('-ref', dest='ref', help="REFERENCE FILE")
	parser.add_argument('-i', dest='input', nargs = '*', action='append', help="INPUT FILE")
	parser.add_argument('-sync', dest='sync', default=0, help="time in s for synchronize input files with reference file (default=0)")
	parser.add_argument('-sw', dest='sync_windows', default = 0, help="synchronisation windows - Try to find the best sync time from the sync time in this time windows (default=0)" )
	parser.add_argument('-deint', dest='deint', default = "auto", help="Scale filter flags (default=auto)" )
	parser.add_argument('-subsampling', dest='subsampling', default = "auto", help="Subsampling value (default=auto)" )
	parser.add_argument('-scale', dest='scale', default = "neighbor", help="Scale filter flags (default=neighbor)" )
	parser.add_argument('-vmaf_model', dest='vmaf_model', default = "auto", help="VMAF Model (default=auto)" )
	parser.add_argument('-loglevel', dest='loglevel', default = "info", help="ffprobe/ffmpeg loglevel" )


	args = parser.parse_args()
	ref_file = args.ref
	all_input = args.input
	sync_time = float(args.sync)
	sync_windows = float(args.sync_windows)
	deint_filter = args.deint
	subsampling = args.subsampling
	scale_filter = args.scale
	vmaf_model = args.vmaf_model
	loglevel = args.loglevel


	os.makedirs(tmp_path, exist_ok=True)

	if ref_file: ##################################################################### ref_file to ref_obj

		print("* Analyzing Reference File...",flush=True)
		ref_obj = manage_ref_file(ref_file, loglevel)

	list_input_obj = [] ##################################################################### list_input_file to list_input_obj

	if all_input and all_input != [['']]:

		print("* Analyzing tests Files...",flush=True)
		list_input_obj = manage_input_files(all_input, loglevel)

		if sync_windows :
			print("* Search sync values...",flush=True)
			print(" ",flush=True)


		for input_obj in list_input_obj:

			input_obj.vmaf_model = vmaf_model
			input_obj.ref_deint = deint_filter
			input_obj.n_subsample = subsampling
			input_obj.scale_filter = scale_filter
			input_obj.sync = sync_time 

	if ref_file and all_input : ############################################################# create quality json (VMAF +PSNR)

		arguments = []

		print("* Quality measures...",flush=True)

		for input_obj in list_input_obj:

			input_obj.ref_file = ref_obj.filename

			if input_obj.ref_deint == "auto":
				set_reference_deint(ref_obj, input_obj)

			if input_obj.n_subsample == "auto": 
				set_subsampling(ref_obj, input_obj)

			if sync_windows :
				input_obj.sync = find_sync_values (ref_obj, input_obj, sync_time, sync_windows)

			set_vmaf_model(ref_obj, input_obj)
			set_scaling_filter(ref_obj, input_obj)
			#arguments.append([ref_obj, input_obj])
			make_quality_info(ref_obj, input_obj, loglevel)
		
		#p.map(call_quality_info, arguments)
		
		for input_obj in list_input_obj: ################################### read quality json 

			try:
				data_json = json.load(open("{0}quality_{1}.json".format( tmp_path , input_obj.name)))
			except:
				with open("{0}quality_{1}.json".format( tmp_path , input_obj.name), 'r') as file : #################### replace nan by 0
					filedata = file.read()
				# Replace the target string
				filedata = filedata.replace("nan", "0")
				# Write the file out again
				with open("{0}quality_{1}.json".format( tmp_path , input_obj.name), 'w') as file:
					file.write(filedata)
				data_json = json.load(open("{0}quality_{1}.json".format( tmp_path , input_obj.name)))

			vmaf_values = []
			psnr_values = []

			for i in range(len(data_json['frames'])):
				try:
					vmaf_values.append(data_json['frames'][i]["metrics"]["vmaf"]) ################################# get vmaf values (libvmaf)
				except Exception:
					pass

				try:
					psnr_values.append(data_json['frames'][i]["metrics"]["psnr"]) ################################# get psnr values (libvmaf)
				except Exception:
					pass

			input_obj.vmaf = vmaf_values
			input_obj.vmaf_avg = round(sum(vmaf_values)/len(vmaf_values), 2)
			input_obj.psnr = psnr_values
			input_obj.psnr_avg = round(sum(psnr_values)/len(psnr_values), 2)

	print("* Results...",flush=True)
	for input_obj in list_input_obj:
		output_json = json.dumps(input_obj.__dict__, sort_keys=True, indent=4)
		print("",flush=True)
		print("-> {0}".format(input_obj.filename),flush=True)
		print(" Bitrate AVG : {0} Mbps".format(input_obj.bitrate_avg),flush=True)
		print(" PSNR AVG : {0}".format(input_obj.psnr_avg),flush=True)
		print(" VMAF AVG : {0}".format(input_obj.vmaf_avg),flush=True)

		######## tests files json output #####
		f = open("{0}/{1}.json".format(input_obj.path, input_obj.name),'w')
		f.write(output_json)
		f.close()
	print("* Done!",flush=True)

	if ref_file:
		######## ref json output #####
		output_json = json.dumps(ref_obj.__dict__, sort_keys=True, indent=4)
		f = open("{0}/{1}.json".format(ref_obj.path, ref_obj.name),'w')
		f.write(output_json)
		f.close()




