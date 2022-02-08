#!/usr/bin/python
# -*- coding: utf-8 -*-

class SpellCaster:
    
    def __init__(self, automation):
        self.automation = automation
        self.complimentaries = {
                'Lumos': 'Nox',
                'Nox': 'Lumos'
            }
        self.spellStates = {
                'Lumos': False,
                'Nox': False
            }
        self.reset()

    def __triggerSpellSensor(self, spell):
        if(not self.__spellAlreadyCasted(spell)):
            self.automation.triggerSpellEffects(spell)
            self.__registerCast(spell)
            
    def __spellAlreadyCasted(self, spell):
        return self.spellStates[spell]
            
    def __registerCast(self, spell):
        #TODO thread safe
        self.spellStates[spell] = True
        if(spell in self.complimentaries):
            comp = self.complimentaries[spell]
            self.spellStates[comp] = False
            
    def detect(self,a,b,c,d,i):
        #print("point: %s" % i)
        #look for basic movements - TODO: trained gestures
        if ((a<(c-5))&(abs(b-d)<2)):
            self.directions[i].append("left")
        elif ((c<(a-5))&(abs(b-d)<2)):
            self.directions[i].append("right")
        elif ((b<(d-5))&(abs(a-c)<5)):
            self.directions[i].append("up")
        elif ((d<(b-5))&(abs(a-c)<5)):
            self.directions[i].append("down")
        astr = ''.join(map(str, self.directions[i]))

        if "upupupup" in astr:
            return "Lumos"
        elif "downdowndowndown" in astr:
            return "Nox"
        return None;
    
    def cast(self, spell):
        self.reset()
        self.casting = True;
        print("CAST: %s" %spell)
        self.__triggerSpellSensor(spell)
        
    def casting(self):
        return self.casting
        
    def reset(self):
        self.casting = False
        self.directions = [[0] for y in range(15)] 