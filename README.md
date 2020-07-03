[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Smart Social Distancing

## Introduction

Smart Distancing is an open-source application to quantify social distancing measures using edge computer vision systems. Since all computation runs on the device, it requires minimal setup and minimizes privacy and security concerns. It can be used in retail, workplaces, schools, construction sites, healthcare facilities, factories, etc.

<div align="center">
  <img  width="100%" src="demo.gif">
</div>

You can run this application on edge devices such as NVIDIA's Jetson Nano / TX2 or Google's Coral Edge-TPU. This application measures social distancing rates and gives proper notifications each time someone ignores social distancing rules. By generating and analyzing data, this solution outputs statistics about high-traffic areas that are at high risk of exposure to COVID-19 or any other contagious virus. The project is under substantial active development; you can find our roadmap at https://github.com/neuralet/neuralet/projects/1.

We encourage the community to join us in building a practical solution to keep people safe while allowing them to get back to their jobs. You can read more about the project motivation and roadmap here: https://docs.google.com/presentation/d/13EEt4JfdkYSqpPLpotx9taBHpNW6WtfXo2SfwFU_aQ0/edit?usp=sharing

Please join [our slack channel](https://neuralet.slack.com/join/shared_invite/zt-ez7x601j-1NehEt5LZxkQFg99ElYXbw#/) or reach out to covid19project@neuralet.com if you have any questions. 


## Getting Started

You can read the [Smart Social Distancing tutorial](https://neuralet.com/docs/tutorials/smart-social-distancing/) on our website. The following instructions will help you get started.

### Prerequisites

**Hardware**  
A host edge device. We currently support the following:
* NVIDIA Jetson Nano
* NVIDIA Jetson TX2
* Coral Dev Board
* AMD64 node with attached Coral USB Accelerator

**Software**
* You should have [Docker](https://docs.docker.com/get-docker/) on your device.

### Install

Make sure you have the prerequisites and then clone this repository to your local system by running this command:

```
git clone https://github.com/neuralet/smart-social-distancing.git
cd smart-social-distancing
```

### Usage

Make sure you have `Docker` installed on your device by following [these instructions](https://docs.docker.com/install/linux/docker-ce/debian).

**Download Required Files**
```
# Download a sample video file from https://megapixels.cc/oxford_town_centre/
./download_sample_video.sh
```

**Building the Docker image for frontend**
(This step is optional if are not going to build any docker image)

All dockerfiles in this repository copy the static files from `neuralet/smart-social-distancing:latest-frontend` to their own  image. If the `frontend` directory on your branch is not identical to
the upstream `master` branch, you MUST build the frontend image with tag "`neuralet/smart-social-distancing:latest-frontend`" BEFORE BUILDING THE MAIN IMAGE.
Otherwise, skip this step, as we have already built the frontend for `master` branch on Dockerhub.

* Building the frontend is resource intensive. If you are using a host edge device, we suggest building the docker image
on your PC/laptop first: 
```
# Run these commands on your PC/laptop:
docker build -f frontend.Dockerfile -t "neuralet/smart-social-distancing:latest-frontend" .
docker save -o "frontend_image.tar" neuralet/smart-social-distancing:latest-frontend
```

* Then, move the file `frontend_image.tar` that was just built on your PC/laptop to your edge device and load it:
```
# Copy "frontend_image.tar" to your edge device and run this command on your device:
docker load -i "frontend_image.tar"
rm frontend_image.tar
```

**Build the run-frontend image**
```
docker build -f run-frontend.Dockerfile -t "neuralet/smart-social-distancing:latest-web-gui" .
docker run -it -p HOST_PORT_FRONTEND:8000 --rm  neuralet/smart-social-distancing:latest-web-gui 
```

**Run on Jetson Nano**
* You need to have JetPack 4.3 installed on your Jetson Nano.

```
# 1) Download TensorRT engine file built with JetPack 4.3:
./download_jetson_nano_trt.sh

# 2) Build Docker image for Jetson Nano (This step is optional, you can skip it if you want to pull the container from neuralet dockerhub)
docker build -f jetson-nano.Dockerfile -t "neuralet/smart-social-distancing:latest-jetson-nano" .

# 3) Run Docker container:
docker run -it --runtime nvidia --privileged -p HOST_PORT:8000 -v "$PWD/data":/repo/data neuralet/smart-social-distancing:latest-jetson-nano
```

**Run on Jetson TX2**
* You need to have JetPack 4.3 installed on your Jetson TX2.

```
# 1) Download TensorRT engine file built with JetPack 4.3:
./download_jetson_tx2_trt.sh

# 2) Build Docker image for Jetson TX2
docker build -f jetson-tx2.Dockerfile -t "neuralet/smart-social-distancing:latest-jetson-tx2" .

# 3) Run Docker container:
docker run -it --runtime nvidia --privileged -p HOST_PORT_API:8000 -v "$PWD/data":/repo/data neuralet/smart-social-distancing:latest-jetson-tx2
```

**Run on Coral Dev Board**
```
# 1) Build Docker image (This step is optional, you can skip it if you want to pull the container from neuralet dockerhub)
docker build -f coral-dev-board.Dockerfile -t "neuralet/smart-social-distancing:latest-coral-dev-board" .
# 2) Run Docker container:
docker run -it --privileged -p HOST_PORT_API:8000 -v "$PWD/data":/repo/data neuralet/smart-social-distancing:latest-coral-dev-board
```

**Run on AMD64 node with a connected Coral USB Accelerator**
```
# 1) Build Docker image (This step is optional, you can skip it if you want to pull the container from neuralet dockerhub)
docker build -f amd64-usbtpu.Dockerfile -t "neuralet/smart-social-distancing:latest-amd64" .
# 2) Run Docker container:
docker run -it --privileged -p HOST_PORT_API:8000 -v "$PWD/data":/repo/data neuralet/smart-social-distancing:latest-amd64
```

**Run on x86**
```
# 1) Build Docker image (This step is optional, you can skip it if you want to pull the container from neuralet dockerhub)
docker build -f x86.Dockerfile -t "neuralet/smart-social-distancing:latest-x86_64" .
# 2) Run Docker container:
docker run -it -p HOST_PORT_API:8000 -v "$PWD/data":/repo/data neuralet/smart-social-distancing:latest-x86_64
```

**Run on x86 using OpenVino**
```
# download model first
./download_openvino_model.sh

# 1) Build Docker image (This step is optional, you can skip it if you want to pull the container from neuralet dockerhub)
docker build -f x86-openvino.Dockerfile -t "neuralet/smart-social-distancing:latest-x86_64_openvino" .
# 2) Run Docker container:
docker run -it -p HOST_PORT_API:8000 -v "$PWD/data":/repo/data neuralet/smart-social-distancing:latest-x86_64_openvino
```

### Configurations
You can read and modify the configurations in `config-jetson.ini` file for Jetson Nano / TX2 and `config-skeleton.ini` file for Coral.

Under the `[Detector]` section, you can modify the `Min score` parameter to define the person detection threshold. You can also change the distance threshold by altering the value of `DistThreshold`.

## Issues and Contributing

The project is under substantial active development; you can find our roadmap at https://github.com/neuralet/neuralet/projects/1. Feel free to open an issue, send a Pull Request, or reach out if you have any feedback.
* [Submit a feature request](https://github.com/neuralet/neuralet/issues/new?assignees=&labels=&template=feature_request.md&title=).
* If you spot a problem or bug, please let us know by [opening a new issue](https://github.com/neuralet/neuralet/issues/new?assignees=&labels=&template=bug_report.md&title=).


## Contact Us

* Visit our website at https://neuralet.com
* Email us at covid19project@neuralet.com
* Check out our other models at https://github.com/neuralet.
