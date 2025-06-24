from .base_agent import BaseAgent

class OrganizationalAssessmentAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model, "Organizational Assessment")