from .base_agent import BaseAgent

class StrategicPlanningAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model, "Strategic Planning")