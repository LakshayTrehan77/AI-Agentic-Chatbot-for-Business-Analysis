from .base_agent import BaseAgent

class OperationalEfficiencyAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model, "Operational Efficiency Analysis")