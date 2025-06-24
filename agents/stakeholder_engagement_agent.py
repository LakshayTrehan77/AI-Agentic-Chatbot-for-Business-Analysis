from .base_agent import BaseAgent

class StakeholderEngagementAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model, "Stakeholder Engagement Strategy")