from BPTK_Py import sd_functions as sd
from .module import Module

class Projects(Module):
    def __init__(self, model, name):
        super().__init__(model, name)

        # Exports
        
        self.projects = self.model.stock(self.module_element("projects"))
        self.deliveringProjects = self.model.flow(self.module_element("deliveringProjects"))
        self.prospectingEffort = self.model.converter(self.module_element("prospectingEffort"))
        self.projectVolume = self.model.converter(self.module_element("projectVolume"))
    
    def initialize(self,staff):
        proposals = self.model.stock(self.module_element("proposals"))
        prospectingProjects = self.model.flow(self.module_element("prospectingProjects"))
        winningProjects = self.model.flow(self.module_element("winningProjects"))
        proposalRate = self.model.converter(self.module_element("proposalRate"))
        projectAcquisitionDuration = self.model.converter(self.module_element("projectAcquisitionDuration"))
        projectDeliveryRate = self.model.converter(self.module_element("projectDeliveryRate"))

        self.projects.initial_value = 320.0
        self.projects.equation = -self.deliveringProjects+winningProjects
        self.deliveringProjects.equation = sd.min(projectDeliveryRate,self.projects)
        projectDeliveryRate.equation = staff.projectDeliveryCapacity

        proposals.initial_value = 320.0
        proposals.equation=prospectingProjects-winningProjects

        self.prospectingEffort.equation = 4.0
        self.projectVolume.equation = 16.0
        proposalRate.equation = self.projectVolume * (staff.businessDevelopmentCapacity/self.prospectingEffort)
        prospectingProjects.equation = proposalRate
        projectAcquisitionDuration.equation = 6.0
        winningProjects.equation = sd.min(sd.delay(self.model,prospectingProjects,projectAcquisitionDuration,160.0),proposals)