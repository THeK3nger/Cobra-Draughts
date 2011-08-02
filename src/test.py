'''
Created on Jul 22, 2011

@author: davide
'''

from draughtscore.DraughtsBrain import DraughtsBrain

weights = {'PIECE':10,
          'KING':30,
          'BACK':1,
          'KBACK':1,
          'CENTER':1,
          'KCENTER':1,
          'FRONT':2,
          'KFRONT':2,
          'MOB':0}

D = DraughtsBrain(weights,4)
D.run_self()

print "The winner is %s!" % D.winner
