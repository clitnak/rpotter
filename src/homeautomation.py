#!/usr/bin/python
# -*- coding: utf-8 -*-


import SmartThings
import requests
import json
import time

class SmartThingsProcessor:
    
    def __init__(self, token, home, spellToDeviceMappings):
        self.token = token
        self.home = home
        self.spellToDeviceNameMappings = spellToDeviceMappings
        self.spellToDeviceIdMappings = {}
        self.smartthingsData = None
        

    def executeDeviceCommand(self, deviceId, capability, command, arguments=None):
        headers = {
            'Accept': 'application/vnd.smartthings+json;v=1',
            'Authorization': 'Bearer ' + self.token,
        }

        response = requests.post(
            'https://api.smartthings.com/devices/' + deviceId + '/commands',
            params=None,
            headers=headers,
            data= json.dumps(
                {
                    "commands":[
                        {
                            'component': 'main',
                            'capability': capability,
                            'command': command,
                            'arguments': []
                        }
                    ]
                }
            )
        )
        #print(response.content)
        #print(response.request.body)
        #return response.raise_for_status()
    def triggerSpellEffects(self, spell):
        self.initialConnectIfNeeded()
        if(spell in self.spellToDeviceIdMappings):
            device = self.spellToDeviceIdMappings[spell]
            self.executeDeviceCommand(device,"switch","on")
            time.sleep(1)
            self.executeDeviceCommand(device,"switch","off")
        else:
            raise ValueError('Spell: ' + spell + ' does not have a device mapping')

    def initialConnectIfNeeded(self):
        if(self.smartthingsData is None):
            self.smartthingsData = SmartThings.Account(self.token)
            for spellName in self.spellToDeviceNameMappings:
                deviceName = self.spellToDeviceNameMappings[spellName]
                deviceHome = self.smartthingsData.devices[self.home]
                if(not deviceName in deviceHome):
                    raise ValueError("Device: '" + deviceName + "' is not in the smartthings home '" + self.home + "'")
                deviceId = deviceHome[deviceName]
                self.spellToDeviceIdMappings[spellName] = deviceId
