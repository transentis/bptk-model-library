from BPTK_Py import sd_functions as sd
from .module import Module

class Kpi(Module):
    def __init__(self, model, name):
        super().__init__(model, name)
        self.targetBusinessDevelopmentAllocationPct = self.model.converter(self.module_element("targetBusinessDevelopmentAllocation%"))
        self.steadyGrowthPolicyOn = self.model.converter(self.module_element("steadyGrowthPolicyOn"))

    
    def initialize(self, staff, cash, projects):
        #kpi
        cashFlowPerProfessional = self.model.converter(self.module_element("cashFlowPerProfessional"))
        utilizationPct = self.model.converter(self.module_element("utilization%"))
        projectBacklog = self.model.converter(self.module_element("projectBacklog"))
        maximumProjectCacpacity = self.model.converter(self.module_element("maximumProjectCapacity"))
        acquisitionToDeliveryRatioPct = self.model.converter(self.module_element("acquisitionToDeliveryRatio%"))
        minimumBusDevAllocationOn = self.model.converter(self.module_element("minimumBusDevAllocationOn"))    

        #kpi targets
        targetProjectStaff = self.model.converter(self.module_element("targetProjectStaff"))
        targetProjectDeliveryCapacity = self.model.converter(self.module_element("targetProjectDeliveryCapacity"))
        targetBacklog = self.model.converter(self.module_element("targetBacklog"))

        cashFlowPerProfessional.equation = cash.cashFlow/staff.professionalStaff
        utilizationPct.equation = (100.0*projects.deliveringProjects)/maximumProjectCacpacity
        projectBacklog.equation =  projects.projects/maximumProjectCacpacity
        maximumProjectCacpacity.equation =(1.0-acquisitionToDeliveryRatioPct/100.0)* staff.professionalStaff
        acquisitionToDeliveryRatioPct.equation = 100.0*projects.prospectingEffort/(projects.prospectingEffort+projects.projectVolume)
        self.steadyGrowthPolicyOn.equation = 0.0
        minimumBusDevAllocationOn.equation = 0.0

        targetProjectStaff.equation = targetProjectDeliveryCapacity
        targetProjectDeliveryCapacity.equation = projects.projects/targetBacklog
        targetBacklog.equation = 2.0
        self.targetBusinessDevelopmentAllocationPct.equation = sd.If(minimumBusDevAllocationOn==0.0,100.0*sd.max(1.0-targetProjectStaff/staff.professionalStaff,0.0),sd.max(100.0*(1.0-targetProjectStaff/staff.professionalStaff),acquisitionToDeliveryRatioPct))