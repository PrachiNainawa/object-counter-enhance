include .env

all: download install clean run

ifeq ($(OS), Windows_NT)
export NUM_PHYSICAL_CORES=$(shell powershell -Command "(Get-WmiObject Win32_Processor | Select-Object -ExpandProperty NumberOfCores)")

run:
	docker-compose up -d
	python -m counter.entrypoints.webapp


install:
	pip install -r requirements.txt


download:
	curl -O storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
	del rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	if exist tmp\model\1 rd /s /q tmp\model\1
	mkdir tmp\model\1
	move tmp\rfcn_resnet101_coco_2018_01_28\saved_model\saved_model.pb tmp\model\1
	rmdir /s /q "tmp/rfcn_resnet101_coco_2018_01_28"


else
cores_per_socket=`lscpu | grep "Core(s) per socket" | cut -d':' -f2 | xargs`
num_sockets=`lscpu | grep "Socket(s)" | cut -d':' -f2 | xargs`
export NUM_PHYSICAL_CORES=$((cores_per_socket * num_sockets))
run:
	docker-compose up -d
	python3 -m counter.entrypoints.webapp


install:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt


download:
	wget -O rfcn_resnet101_fp32_coco_pretrained_model.tar.gz https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
	rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
	mkdir -p tmp/model/1
	mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/1
	rm -rf tmp/rfcn_resnet101_coco_2018_01_28


endif


test:
	pytest


pep8_test:
	pytest --flakes
	pytest --pycodestyle


clean:
	docker-compose down


shutdown:
	docker-compose stop