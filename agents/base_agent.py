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

        Generate a detailed and comprehensive final response for the task based on the company information and user answers to questions. Provide in-depth, actionable insights relevant to the task, including specific recommendations, potential challenges, and strategic considerations. Structure the response with clear sections (e.g., Overview, Key Insights, Recommendations, Conclusion) to ensure clarity and depth.
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

        Generate a concise response to the follow-up question, ensuring relevance to the task and company context. Keep the response brief, focused, and directly addressing the user's query.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return "Unable to process follow-up question."
