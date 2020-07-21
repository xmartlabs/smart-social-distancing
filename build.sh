#!/usr/bin/env bash
# Precondition: Docker is installed on the device

DEVICES="jetson_nano jetson_tx2 coral_dev_board amd64_coral_usb_accelerator cpu_x86 intel_cpu_x86_openvino"

echo ''
echo "----------------------------------"
echo "STEP 1/3: Downloading video sample"
echo "----------------------------------"
echo ''
read -p "Do you wish to download the video sample? (Default is yes) (y/n) " -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]
then
  . download_sample_video.sh
fi

echo ''
echo "-------------------------------"
echo "STEP 2/3: Build frontend images"
echo "-------------------------------"
echo ''
echo ""
read -p "Do you wish to build the frontend images? (Default is yes) (y/n) " -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]
then
    echo 'Building frontend images'
    docker build -f frontend.Dockerfile -t "neuralet/smart-social-distancing:latest-frontend" .
    docker build -f run-frontend.Dockerfile -t "neuralet/smart-social-distancing:latest-web-gui" .
fi

echo ''
echo "-------------------------------"
echo "STEP 3/3: Build processor image"
echo "-------------------------------"
echo ''
echo "Please select your device from the following list:"
select device in $DEVICES
do
  # TODO: LANTHORN-4: Create run_backend.sh file for the specified device. Add it to .gitignore
  case $device in
    jetson_nano)
        . download_jetson_nano_trt.sh
        docker build -f jetson-nano.Dockerfile -t "neuralet/smart-social-distancing:latest-jetson-nano" .
        break
        ;;
    jetson_tx2)
        . download_jetson_tx2_trt.sh
        docker build -f jetson-tx2.Dockerfile -t "neuralet/smart-social-distancing:latest-jetson-tx2" .
        break
        ;;
    coral_dev_board)
        docker build -f coral-dev-board.Dockerfile -t "neuralet/smart-social-distancing:latest-coral-dev-board" .
        break
        ;;
    amd64_coral_usb_accelerator)
        docker build -f amd64-usbtpu.Dockerfile -t "neuralet/smart-social-distancing:latest-amd64" .
        break
        ;;
    cpu_x86)
        docker build -f x86.Dockerfile -t "neuralet/smart-social-distancing:latest-x86_64" .
        break
        ;;
    intel_cpu_x86_openvino)
        . download_openvino_model.sh
        docker build -f x86-openvino.Dockerfile -t "neuralet/smart-social-distancing:latest-x86_64_openvino" .
        break
        ;;
    * )
      echo "Please select a listed device."
      ;;
  esac
done

echo ''
echo "---------------------"
echo "Build has finished :)"
echo "---------------------"
echo ''
