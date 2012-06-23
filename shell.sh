#!/bin/bash
ipython -i -c "from model import *; from mongoengine import connect; connect('uppsalabarn')" 
