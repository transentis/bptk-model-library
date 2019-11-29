
#      _                   _ _
#  _____| |__ ___ _ __  _ __(_| |___ _ _
# (_-/ _` / _/ _ | '  \| '_ | | / -_| '_|
# /__\__,_\__\___|_|_|_| .__|_|_\___|_|
#                      |_|
# Copyright (c) 2013-2016 transentis management & consulting. All rights reserved.
#
from BPTK_Py.sdcompiler.sdmodel import LERP, SDModel
import numpy as np
from scipy.interpolate import interp1d
import math, statistics
import random

def random_with_seed(seed):
    random.seed(seed)
    return random.random()



class simulation_model(SDModel):
  def memoize(self, equation, arg):
    mymemo = self.memo[equation]
    if arg in mymemo.keys():
      return mymemo[arg]
    else:
      result = self.equations[equation](arg)
      mymemo[arg] = result

    return result

  def __init__(self):
    # Simulation Buildins
    self.dt = 0.25
    self.starttime = 1
    self.stoptime = 61
    self.equations = {

    # Stocks
    

    'expectedPrice'          : lambda t: ( (3.0) if ( t  <=  self.starttime ) else (self.memoize('expectedPrice',t-self.dt) + self.dt * ( self.memoize('changeInExpectedPrice',t-self.dt) )) ),
    'expectedProfitabilityOfCurrentOperations'          : lambda t: ( (100.0) if ( t  <=  self.starttime ) else (self.memoize('expectedProfitabilityOfCurrentOperations',t-self.dt) + self.dt * ( self.memoize('changeInProfitExpectation',t-self.dt) )) ),
    'inventory'          : lambda t: ( (300.0) if ( t  <=  self.starttime ) else (self.memoize('inventory',t-self.dt) + self.dt * ( self.memoize('productionRate',t-self.dt) - ( self.memoize('consumptionRate',t-self.dt) ) )) ),
    'perceivedInventoryCoverage'          : lambda t: ( (3.0) if ( t  <=  self.starttime ) else (self.memoize('perceivedInventoryCoverage',t-self.dt) + self.dt * ( self.memoize('changeInPerceivedInventoryCoverage',t-self.dt) )) ),
    'production'          : lambda t: ( (300.0) if ( t  <=  self.starttime ) else (self.memoize('production',t-self.dt) + self.dt * ( self.memoize('productionStartRate',t-self.dt) - ( self.memoize('productionRate',t-self.dt) ) )) ),
    'productionCapacity'          : lambda t: ( (200.0) if ( t  <=  self.starttime ) else (self.memoize('productionCapacity',t-self.dt) + self.dt * 0) ),
    

    # Flows
    'changeInExpectedPrice'             : lambda t: max( ( self.memoize('indicatedPrice', t) - self.memoize('expectedPrice', t) ) / self.memoize('priceAdjustmentTime', t) , 0.0),
    'changeInPerceivedInventoryCoverage'             : lambda t: ( self.memoize('inventoryCoverage', t) - self.memoize('perceivedInventoryCoverage', t) ) / self.memoize('inventoryCoveragePerceptionTime', t),
    'changeInProfitExpectation'             : lambda t: ( self.memoize('profit', t) - self.memoize('expectedProfitabilityOfCurrentOperations', t) ) / self.memoize('profitAdjustmentTime', t),
    'consumptionRate'             : lambda t: max( 0 , min( self.memoize('inventory', t) , self.memoize('demand', t))),
    'productionRate'             : lambda t: max( 0 , min( self.memoize('production', t) , ( (100.0)  if t - self.starttime < (self.memoize('productionTime', t)) else (self.memoize('productionStartRate', ( t - (self.memoize('productionTime', t)) ))) ) )),
    'productionStartRate'             : lambda t: max( 0 , self.memoize('capacityUtilization', t) * self.memoize('productionCapacity', t)),
    

    # converters
    'capacityCost'      : lambda t: self.memoize('unitCapacityCost', t) * self.memoize('productionCapacity', t),
    'capacityUtilization'      : lambda t: self.memoize('effectOfProfitabilityOnCapacityUtilization', t),
    'costs'      : lambda t: self.memoize('variableCosts', t) + self.memoize('capacityCost', t),
    'demand'      : lambda t: self.memoize('effectOfRelativeValueOnDemand', t) * self.memoize('referenceDemand', t),
    'indicatedPrice'      : lambda t: max( self.memoize('price', t) , self.memoize('minimumPrice', t)),
    'inventoryCoverage'      : lambda t: self.memoize('inventory', t) / self.memoize('consumptionRate', t),
    'inventoryCoveragePerceptionTime'      : lambda t: 3.0,
    'marketShockOn'      : lambda t: 0.0,
    'minimumPrice'      : lambda t: self.memoize('unitVariableCost', t) + self.memoize('unitCapacityCost', t),
    'price'      : lambda t: self.memoize('expectedPrice', t) * self.memoize('effectOfInventoryCoverageOnPrice', t),
    'priceAdjustmentTime'      : lambda t: 3.0,
    'priceOfSubstitutes'      : lambda t: 3.0,
    'productionTime'      : lambda t: 3.0,
    'profit'      : lambda t: self.memoize('revenue', t) - self.memoize('costs', t),
    'profitAdjustmentTime'      : lambda t: 12.0,
    'referenceDemand'      : lambda t: 100.0 + self.memoize('marketShockOn', t) * (0 if t < 10.0 else 50.0),
    'referenceExpectedProfitability'      : lambda t: 100.0,
    'referenceInventoryCoverage'      : lambda t: 3.0,
    'relativeExpectedProfitability'      : lambda t: self.memoize('expectedProfitabilityOfCurrentOperations', t) / self.memoize('referenceExpectedProfitability', t),
    'relativeInventoryCoverage'      : lambda t: self.memoize('perceivedInventoryCoverage', t) / self.memoize('referenceInventoryCoverage', t),
    'relativeValueOfProduct'      : lambda t: self.memoize('priceOfSubstitutes', t) / self.memoize('price', t),
    'revenue'      : lambda t: self.memoize('consumptionRate', t) * self.memoize('price', t),
    'unitCapacityCost'      : lambda t: 0.5,
    'unitVariableCost'      : lambda t: 1.0,
    'variableCosts'      : lambda t: self.memoize('unitVariableCost', t) * self.memoize('productionRate', t),
    

    # gf
    'effectOfInventoryCoverageOnPrice' : lambda t: LERP( self.memoize('relativeInventoryCoverage', t), self.points['effectOfInventoryCoverageOnPrice']),
    'effectOfProfitabilityOnCapacityUtilization' : lambda t: LERP( self.memoize('relativeExpectedProfitability', t), self.points['effectOfProfitabilityOnCapacityUtilization']),
    'effectOfRelativeValueOnDemand' : lambda t: LERP( self.memoize('relativeValueOfProduct', t), self.points['effectOfRelativeValueOnDemand']),
    

    #constants
    


    }

    self.points = {
        'effectOfInventoryCoverageOnPrice' :  [(0.0, 1.404), (0.16666666666666666, 1.415), (0.3333333333333333, 1.404), (0.5, 1.372), (0.6666666666666666, 1.351), (0.8333333333333334, 1.277), (1.0, 1.0), (1.1666666666666667, 0.787), (1.3333333333333333, 0.798), (1.5, 0.809), (1.6666666666666667, 0.787), (1.8333333333333333, 0.766), (2.0, 0.766)]  , 'effectOfProfitabilityOnCapacityUtilization' :  [(0.0, 0.324), (0.16666666666666666, 0.33), (0.3333333333333333, 0.372), (0.5, 0.394), (0.6666666666666666, 0.41), (0.8333333333333334, 0.42), (1.0, 0.5), (1.1666666666666667, 0.745), (1.3333333333333333, 0.80075), (1.5, 0.8565), (1.6666666666666667, 0.91225), (1.8333333333333333, 0.968), (2.0, 0.968)]  , 'effectOfRelativeValueOnDemand' :  [(0.0, 0.564), (0.16666666666666666, 0.521), (0.3333333333333333, 0.532), (0.5, 0.564), (0.6666666666666666, 0.67), (0.8333333333333334, 0.745), (1.0, 1.0), (1.1666666666666667, 1.362), (1.3333333333333333, 1.479), (1.5, 1.574), (1.6666666666666667, 1.638), (1.8333333333333333, 1.66), (2.0, 1.66)]  , 
    }


    self.dimensions = {
  	 }

    self.stocks = ['expectedPrice',  'expectedProfitabilityOfCurrentOperations',  'inventory',  'perceivedInventoryCoverage',  'production',  'productionCapacity',  ]
    self.flows = ['changeInExpectedPrice',  'changeInPerceivedInventoryCoverage',  'changeInProfitExpectation',  'consumptionRate',  'productionRate',  'productionStartRate',  ]
    self.converters = ['capacityCost',  'capacityUtilization',  'costs',  'demand',  'indicatedPrice',  'inventoryCoverage',  'inventoryCoveragePerceptionTime',  'marketShockOn',  'minimumPrice',  'price',  'priceAdjustmentTime',  'priceOfSubstitutes',  'productionTime',  'profit',  'profitAdjustmentTime',  'referenceDemand',  'referenceExpectedProfitability',  'referenceInventoryCoverage',  'relativeExpectedProfitability',  'relativeInventoryCoverage',  'relativeValueOfProduct',  'revenue',  'unitCapacityCost',  'unitVariableCost',  'variableCosts',  ]
    self.gf = ['effectOfInventoryCoverageOnPrice',  'effectOfProfitabilityOnCapacityUtilization',  'effectOfRelativeValueOnDemand',  ]
    self.constants= []
    self.events = [
    	]

    self.memo = {}
    for key in list(self.equations.keys()):
      self.memo[key] = {}  # DICT OF DICTS!

  def specs(self):
    return self.starttime, self.stoptime, self.dt, 'months', 'Euler'
