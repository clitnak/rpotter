#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
'''
import camera
import homeautomation
import spells
import cv2
import wandtracker

########### PARAMETERS #############

# Smartthings token
tokenFile = open("../smartthings-token.txt", "r") 
token = tokenFile.readline().rstrip("\n")

# display intra-processing images 1 through 12
display=12

# Which spells trigger which devices
spellToDeviceMappings = {
    "Nox": "SpellNoxSensor",
    "Lumos": "SpellLumosSensor"
}

########## END PARAMETERS ##########

cam = camera.Camera(True,12)

automation = homeautomation.SmartThingsProcessor(token, 'My home', spellToDeviceMappings)

caster = spells.SpellCaster(automation)

tracker = wandtracker.Tracker(cam, caster)
tracker.start()
tracker.trackAndWait()
cam.end()
