class BaseAgent:
    def __init__(self, model, task_name):
        self.model = model
        self.task_name = task_name

    def generate_final_response(self, conversation_history, company_info, answers):
        prompt = f"""
        Task: {self.task_name}
        Company Info: {company_info}
        User Answers: {answers}
        History: {conversation_history}

        Generate a concise final response for the task based on the company information and user answers to questions. Provide actionable insights relevant to the task.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_follow_up_response(self, conversation_history, company_info, user_input):
        prompt = f"""
        Task: {self.task_name}
        Company Info: {company_info}
        User Follow-Up: {user_input}
        History: {conversation_history}

        Generate a concise response to the follow-up question, ensuring relevance to the task and company context.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return "Unable to process follow-up question."