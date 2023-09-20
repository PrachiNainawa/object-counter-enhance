all: download install clean build run
model_name := rfcn
num_physical_cores := 10
VOL := $(subst /,\,${CURDIR})\tmp\model:/models/$(model_name)

ifeq ($(OS), Windows_NT)
run:
	docker start tfserving
	docker start test-mongo
	docker start postgres-cont
	python -m counter.entrypoints.webapp


install:
	pip install -r requirements.txt


test:
	curl -F "threshold=0.9" -F "file=@resources/images/boy.jpg" http://127.0.0.1:5000/object-count
	curl -F "threshold=0.9" -F "file=@resources/images/cat.jpg" http://127.0.0.1:5000/object-count
	curl -F "threshold=0.9" -F "file=@resources/images/food.jpg" http://127.0.0.1:5000/object-count
	pytest


build:
	docker container create --name=tfserving -p 8500:8500 -p 8501:8501 -v "$(VOL)" -e MODEL_NAME=$(model_name) -e OMP_NUM_THREADS=$(num_physical_cores) -e TENSORFLOW_INTER_OP_PARALLELISM=2 -e TENSORFLOW_INTRA_OP_PARALLELISM=$(num_physical_cores) tensorflow/serving:latest
	docker container create --name test-mongo -p 27017:27017 mongo:6.0
	docker container create -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=prod_counter -p 5432:5432 --name postgres-cont postgres:latest


clean:
	docker rm -f test-mongo
	docker rm -f tfserving
	docker rm -f postgres-cont


download:
	curl -O storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
	del rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	if exist tmp\model\1 rd /s /q tmp\model\1
	mkdir tmp\model\1
	move tmp\rfcn_resnet101_coco_2018_01_28\saved_model\saved_model.pb tmp\model\1
	rmdir /s /q "tmp/rfcn_resnet101_coco_2018_01_28"
	

shutdown:
	docker stop tfserving
	docker stop test-mongo
	docker stop postgres-cont

else
run:
	
	docker start tfserving
	docker start test-mongo
	docker start postgres-cont
	python -m counter.entrypoints.webapp


install:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

test:
	curl -F "threshold=0.9" -F "file=@resources/images/boy.jpg" http://127.0.0.1:5000/object-count
	curl -F "threshold=0.9" -F "file=@resources/images/cat.jpg" http://127.0.0.1:5000/object-count
	curl -F "threshold=0.9" -F "file=@resources/images/food.jpg" http://127.0.0.1:5000/object-count
	pytest
	
build:
	cores_per_socket=`lscpu | grep "Core(s) per socket" | cut -d':' -f2 | xargs`
	num_sockets=`lscpu | grep "Socket(s)" | cut -d':' -f2 | xargs`
	num_physical_cores=$((cores_per_socket * num_sockets))
	docker container create --name=tfserving -p 8500:8500 -p 8501:8501 -v "$(pwd)/tmp/model:/models/$(model_name)" -e MODEL_NAME=$(model_name) -e OMP_NUM_THREADS=$(num_physical_cores) -e TENSORFLOW_INTER_OP_PARALLELISM=2 -e TENSORFLOW_INTRA_OP_PARALLELISM=$(num_physical_cores) tensorflow/serving:latest
	docker container create --name test-mongo -p 27017:27017 mongo:6.0
	docker container create -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=prod_counter -p 5432:5432 --name postgres-cont postgres:latest


clean:
	docker rm -f test-mongo
	docker rm -f tfserving
	docker rm -f postgres-cont


download:
	wget -O rfcn_resnet101_fp32_coco_pretrained_model.tar.gz https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
	rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
	mkdir -p tmp/model/1
	mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/1
	rm -rf tmp/rfcn_resnet101_coco_2018_01_28


shutdown:
	docker stop tfserving
	docker stop test-mongo
	docker stop postgres-cont

endif