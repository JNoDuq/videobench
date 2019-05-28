
# VideoBench (VMAF PSNR Bitrate Analyzer)

## Abstract

Video Bench is a tool that makes it easy to compare transcoded video files with a reference file (source)

* Calculate VMAF and PSNR scores for test files
* Find the real video bitrate (size of the frames and not the size of the packets)
* Give a by seconds or by frames views
* Works with almost all video codecs (mpeg2, H264, HEVC, VP9, ...)
* No need to uncompress the video files
* Can synchronize tests files with reference file
* Choose automatically the right deinterlace filter for the reference file depending of the test file
* Automatically scale the test files for matching the reference file
* Automatically choose the right VMAF model (standard or 4k) depending of the reference file
* Generate a JSON files compiling all the infos
* Easy to install (need Docker and Python3 with the pyside2 library)
* Run on Linux, Mac and windows
* Has a GUI
* Can be used in commande line 


![Video Bench](https://user-images.githubusercontent.com/10562413/57775568-a0f9e780-771d-11e9-8b19-17a0a0b5cd25.png)


## How to install

### Install prerequisites on Linux

#### Install Docker

[Install Docker](https://docs.docker.com/)

#### Make sure you can run a docker container 

```
sudo usermod -a -G docker $USER
```

#### Install python3

```
sudo apt-get install python3
```

#### Install pyside2

```
sudo apt-get install python3-pip
pip3 install pyside2
```

### Install prerequisites on Mac OS 

#### Install Docker

[Install Docker](https://docs.docker.com/)

#### Install python3

```
brew install python3
```

#### Install pyside2

```
brew install python3-pip
pip3 install pyside2
```

### Install prerequisites on Windows 

#### Install Docker

For be able to use Docker on windows you need to have Windows 10 64bit Pro, Enterprise or Education

[Install Docker](https://docs.docker.com/)

#### Install python3

[Install python3](https://www.python.org/downloads/windows/)
Don't forget to click on "add python to PATH"

#### Install pyside2

```
pip install pyside2
```

### Create docker container

Download or clone the repo

```
cd videobench
docker build -t  docker-videobench -f ./Dockerfile ./
```

## How to use it

### Using the GUI 

Run the GUI
```
python3 videobench_ui.py
```
or on windows 

```
python videobench_ui.py
```

![Video Bench GUI overview](https://user-images.githubusercontent.com/10562413/57775395-35b01580-771d-11e9-910a-0eb53eea5959.png)

* You can choose one reference file (Original Video) and multiple tests files (Compressed Videos)
* If your tests files are not synchronize with the reference file you can set the sync time in seconds.
* If your not sure about what sync time is excately the right one, you can set a sync windows. The analyzer will try to find the best sync time, starting by the sync time set and seraching in that windows.
* Click on the start button for start the analyze, when it's done the information and the graph will be showed in the GUI.
* Generate the quality information can take some time, but when it's done all the information will be save in JSON files in the same folder than the video files.
* You can directly import the JSON files in the GUI by using the "Import Measurements" button.

For more information read the article on [Video Bench](https://medium.com/@jnoduq/video-bench-how-measure-your-video-quality-easily-85a0feb8f6e2)

### Using the command line

example :
```
python3 videobench.py -ref ref_files.mp4 -i test_file1.mp4 test_file2.mp4 test_file2.mp4 -sync -0.1 -sw 0.2 
```

help :
```
python3 videobench.py -h
```



















