from BPTK_Py import sd_functions as sd
from .module import Module

class Cost(Module):
    def __init__(self, model, name):
        super().__init__(model, name)
        #Exports
        self.cost = self.model.converter(self.module_element("cost"))
    
    def initialize(self,staff):
        staffSalary = self.model.converter(self.module_element("staffSalary"))
        workplaceCost = self.model.converter(self.module_element("workplaceCost"))
        staffCost = self.model.converter(self.module_element("staffCost"))
        overheadCost = self.model.converter(self.module_element("overheadCost"))

        workplaceCost.equation=1.0
        staffSalary.equation = 80.0/12
        overheadCost.equation = 306.0
        staffCost.equation = staff.professionalStaff*(workplaceCost+staffSalary)
        self.cost.equation=staffCost+overheadCost
