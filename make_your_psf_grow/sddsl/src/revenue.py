from BPTK_Py import sd_functions as sd
from .module import Module

class Revenue(Module):
    def __init__(self, model, name):
        super().__init__(model, name)

        # Exports
        self.collectingRevenue = self.model.flow(self.module_element("collectingRevenue"))
    
    def initialize(self,projects):
        receivables = self.model.stock(self.module_element("receivables"))
        makingRevenue = self.model.flow(self.module_element("makingRevenue"))
        collectionTime = self.model.converter(self.module_element("collectionTime"))
        revenue = self.model.converter(self.module_element("revenue"))
        projectDeliveryFee = self.model.converter(self.module_element("projectDeliveryFee"))

        receivables.initial_value = 160*17.6*2
        receivables.equation = makingRevenue-self.collectingRevenue
        projectDeliveryFee.equation = 17.6
        revenue.equation = projectDeliveryFee*projects.deliveringProjects
        makingRevenue.equation = revenue

        collectionTime.equation=2.0
        self.collectingRevenue.equation=sd.delay(self.model,makingRevenue,collectionTime,160*17.6)