from BPTK_Py import sd_functions as sd
from .module import Module

class Cash(Module):
    def __init__(self, model, name):
        super().__init__(model, name)
        self.cashFlow = self.model.converter(self.module_element("cashFlow"))
        
    
    def initialize(self,cost,revenue):
        cash = self.model.stock(self.module_element("cash"))
        cashIn = self.model.flow(self.module_element("cashIn"))
        cashOut= self.model.flow(self.module_element("cashOut"))
        minimumCash = self.model.converter(self.module_element("minimumCash"))
        easyTargetCash = self.model.converter(self.module_element("easyTargetCash"))
        expertTargetCash = self.model.converter(self.module_element("expertTargetCash"))

        cash.initial_value=1000.0
        cashIn.equation=revenue.collectingRevenue
        cashOut.equation = cost.cost
        cash.equation = cashIn-cashOut
        self.cashFlow.equation = cashIn -cashOut
        minimumCash.equation = 23463.0
        easyTargetCash.equation = 30000.0
        expertTargetCash.equation = 40000.0