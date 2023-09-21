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


# give input

To use any internal tf model, change MODEL_NAME variable and MODEL_PATH to speify input path of the SavedModel folder in .env file
eg: acceptible format - model.save('/path')
change any other env variable through .env file


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
mingw32-make run (runs docker container and flask server)
mingw32-make test (testing)
mingw32-make clean (delete docker containers)
mingw32-make shutdown (stops the container without removing the internal data)
```


# test in new terminal
```
mingw32-make test (tests the functionality)
mingw32-make pep8_test (tests the code quality)
pytest -k e2e (e2e is a keyword in test filename which will only run that particular test, you can change the keyword as per file)
pytest --cov counter (gives info about test coverage of the code for each file)

```
