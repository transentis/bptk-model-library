from BPTK_Py import sd_functions as sd
from .module import Module

class Staff(Module):
    def __init__(self, model, name):
        super().__init__(model, name)

        # Exports
        
        self.professionalStaff = self.model.stock(self.module_element("professionalStaff"))
        self.projectDeliveryCapacity= self.model.converter(self.module_element("projectDeliveryCapacity"))
        self.businessDevelopmentCapacity = self.model.converter(self.module_element("businessDevelopmentCapacity"))
        
    def initialize(self,kpi):

        staffInRecruitment = self.model.stock(self.module_element("staffInRecruitment"))
        hiringStaff = self.model.flow(self.module_element("hiringStaff"))
        staffArriving = self.model.flow(self.module_element("staffArriving"))
        workMonth = self.model.converter(self.module_element("workMonth"))
        workCapacity = self.model.converter(self.module_element("workCapacity"))
        businessDevelopmentAllocationPct = self.model.converter(self.module_element("businessDevelopmentAllocation%"))
        hiringRate = self.model.converter(self.module_element("hiringRate"))
        hiringDuration = self.model.converter(self.module_element("hiringDuration"))
        steadyGrowthRatePct= self.model.converter(self.module_element("steadyGrowthRate%"))
        actualBusinessDevelopmentAllocationPct = self.model.converter(self.module_element("actualBusinessDevelopmentAllocation%"))

        self.professionalStaff.initial_value = 200.0
        self.projectDeliveryCapacity.equation = workCapacity*(100.0 - actualBusinessDevelopmentAllocationPct)/100.0
        actualBusinessDevelopmentAllocationPct.equation = sd.If(kpi.steadyGrowthPolicyOn==1.0,kpi.targetBusinessDevelopmentAllocationPct,businessDevelopmentAllocationPct)
        workMonth.equation=1.0
        workCapacity.equation=self.professionalStaff*workMonth
        businessDevelopmentAllocationPct.equation = sd.lookup(sd.time(),self.module_element("businessDevelopmentAllocation%"))
        self.businessDevelopmentCapacity.equation = workCapacity * actualBusinessDevelopmentAllocationPct/100.0
        self.projectDeliveryCapacity.equation = workCapacity-self.businessDevelopmentCapacity
        self.model.points[self.module_element("businessDevelopmentAllocation%")]=[(1, 20), (2, 20), (3, 20), (4, 20), (5, 20), (6, 
  20), (7, 20), (8, 20), (9, 20), (10, 20), (11, 20), (12, 
  20), (13, 20), (14, 20), (15, 20), (16, 20), (17, 20), (18, 
  20), (19, 20), (20, 20), (21, 20), (22, 20), (23, 20), (24, 
  20)]
        self.model.points[self.module_element("hiringRate")]= [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 
  0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 
  0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 
  0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0), (24, 
  0)]
        staffInRecruitment.initial_value=0.0
        staffInRecruitment.equation = hiringStaff-staffArriving
        self.professionalStaff.equation = staffArriving
        hiringStaff.equation = sd.If(kpi.steadyGrowthPolicyOn==0.0, hiringRate,self.professionalStaff*(steadyGrowthRatePct/100.0))
        staffArriving.equation = sd.delay(self.model, hiringStaff, hiringDuration,0.0)
        hiringRate.equation = sd.lookup(sd.time(),self.module_element("hiringRate"))
        hiringDuration.equation = 3.0
        steadyGrowthRatePct.equation = 1.0


