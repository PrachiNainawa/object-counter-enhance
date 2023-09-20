# Machine Learning & Hexagonal Architecture

The goal of this repo is demonstrate how to apply Hexagonal Architecture in a ML based system 

The model used in this example has been taken from 
[IntelAI](https://github.com/IntelAI/models/blob/master/docs/object_detection/tensorflow_serving/Tutorial.md)


# Prerequisite - 

Docker
Python
Makefile(by default should be available for linux) https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows
Anaconda(if you don't have makefile) https://docs.anaconda.com/free/anaconda/install/index.html


# create anaconda env and install make if you don't have it (windows)

open anaconda prompt and run below cmds

```
conda create --name myenv python=3.11.5
conda activate myenv
conda install -c conda-forge m2w64-make

```


# give input (needed for windows)

open the Makefile and change the num_physical_cores as per your machine
press ctrl+shift+esc to open task manager, click performance to find the cores
if you want to use any other model then change the model_name variable and also the VOl variable to speify input path to the saved model (VOL=<host_path>:<docker_path>)
internally trained model should be in SavedModel format of tf
model.save('saved_model/model_name')

# run the app

run below cmd in the conda env which you created above, use ctrl+c to stop the server
this cmd is tested fully for windows, for linux users please test and debug if any error comes
Note :- linux users can use make keyword instead of mingw32-make

```
mingw32-make all #(all pre-installations and start your flask server)

```
if you don't want to run from scratch you can use below cmds to run particular steps
```
mingw32-make download (download the model)
mingw32-make install (installs the python libraries)
mingw32-make build (builds the docker images)
mingw32-make run (runs docker container and flask server)
mingw32-make test (testing)
mingw32-make clean (delete docker containers)
mingw32-make shutdown (stops the container without removing the internal data)
```


# test in new terminal
```
mingw32-make test 

```
