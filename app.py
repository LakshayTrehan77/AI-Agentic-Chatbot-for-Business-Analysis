import streamlit as st
import google.generativeai as genai
import json
import os
import logging
from dotenv import load_dotenv
from agents.strategic_planning_agent import StrategicPlanningAgent
from agents.organizational_assessment_agent import OrganizationalAssessmentAgent
from agents.operational_efficiency_agent import OperationalEfficiencyAgent
from agents.stakeholder_engagement_agent import StakeholderEngagementAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env
load_dotenv()

# Try to get Gemini API key: first from Streamlit secrets, then .env
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
except (AttributeError, KeyError):
    logging.info("GEMINI_API_KEY not found in Streamlit secrets, falling back to .env")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# If key is still not found, show error and stop
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Please set it in Streamlit secrets or .env.")
    logging.error("GEMINI_API_KEY not found in Streamlit secrets or .env")
    st.stop()

# Configure Gemini API
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    logging.info("Gemini API configured successfully")
except Exception as e:
    st.error(f"Failed to configure Gemini API: {str(e)}")
    logging.error(f"Gemini API configuration failed: {str(e)}")
    st.stop()

# Track API calls
if 'api_call_count' not in st.session_state:
    st.session_state.api_call_count = 0

def increment_api_call():
    st.session_state.api_call_count += 1
    logging.info(f"API call count incremented to {st.session_state.api_call_count}")

# Dictionary mapping task names to agent classes
AGENT_CLASSES = {
    "Strategic Planning": StrategicPlanningAgent,
    "Organizational Assessment": OrganizationalAssessmentAgent,
    "Operational Efficiency Analysis": OperationalEfficiencyAgent,
    "Stakeholder Engagement Strategy": StakeholderEngagementAgent
}

# Normalize company info for consistent cache key
def normalize_company_info(company_info):
    return {
        "name": company_info.get("name", ""),
        "industry": company_info.get("industry", ""),
        "size": company_info.get("size", ""),
        "description": company_info.get("description", "")
    }

# Generate up to 5 questions (MCQ, Radio, Input) with fallback
def generate_task_questions(task, company_info):
    logging.info(f"Generating questions for task: {task} with company info: {company_info}")
    company_info_str = ", ".join(f"{k}: {v}" for k, v in company_info.items() if v)
    prompt = f"""
    Task: {task}
    Company Info: {company_info_str}

    Generate up to 5 short questions (max 15 words each) about the company for the task, including:
    - At least 1 MCQ with 4 options.
    - At least 1 Radio question with 3 options.
    - At least 1 Input-type question (short text input).
    - Focus on company details relevant to the task.
    - Ensure questions elicit detailed insights for a comprehensive {task} analysis.

    Output as JSON array:
    [
        {{
            "type": "MCQ" or "Radio" or "Input",
            "question": "Question text",
            "options": ["Option1", "Option2", ...] (for MCQ and Radio only)
        }}
    ]
    """

    try:
        response = model.generate_content(prompt)
        increment_api_call()
        response_text = getattr(response, 'text', '').strip()

        # Strip markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text.lstrip("```json").rstrip("```").strip()
        elif response_text.startswith("```"):
            response_text = response_text.strip("```").strip()

        logging.info(f"Cleaned response: {response_text}")

        try:
            questions = json.loads(response_text)
            valid_questions = []
            for q in questions:
                if "type" in q and "question" in q:
                    if q["type"] in ["MCQ", "Radio"] and "options" in q:
                        valid_questions.append(q)
                    elif q["type"] == "Input":
                        q.setdefault("options", [])
                        valid_questions.append(q)

            if valid_questions:
                logging.info(f"Generated {len(valid_questions)} valid questions")
                return valid_questions[:5]
            else:
                logging.warning("No valid questions found in the response")
                return fallback_questions()

        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed: {str(e)}")
            return fallback_questions()

    except Exception as e:
        logging.error(f"Question generation failed: {str(e)}")
        return fallback_questions()

# Fallback question list
def fallback_questions():
    logging.info("Using fallback questions")
    return [
        {"type": "MCQ", "question": "What is the company's main focus?", "options": ["AI", "Finance", "Retail", "Healthcare"]},
        {"type": "Radio", "question": "Is the company profitable?", "options": ["Yes", "No", "Unsure"]},
        {"type": "Input", "question": "Describe your key product.", "options": []}
    ]

# Streamlit app
def main():
    st.set_page_config(page_title="AI Business Analysis", layout="wide")
    st.title("AI Agentic Chatbot for Business Analysis")
    st.markdown("Analyze your company with tasks like Strategic Planning, Organizational Assessment, Operational Efficiency, and Stakeholder Engagement.")

    # Initialize session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'company_info' not in st.session_state:
        st.session_state.company_info = {}
    if 'selected_task' not in st.session_state:
        st.session_state.selected_task = None
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'question_phase' not in st.session_state:
        st.session_state.question_phase = True
    if 'questions_asked' not in st.session_state:
        st.session_state.questions_asked = 0
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'final_response_generated' not in st.session_state:
        st.session_state.final_response_generated = False
    if 'follow_up_count' not in st.session_state:
        st.session_state.follow_up_count = 0
    if 'max_follow_ups' not in st.session_state:
        st.session_state.max_follow_ups = 5
    if 'last_company_info' not in st.session_state:
        st.session_state.last_company_info = {}
    if 'last_task' not in st.session_state:
        st.session_state.last_task = None
    if 'ratings' not in st.session_state:
        st.session_state.ratings = {}
    if 'show_follow_up' not in st.session_state:
        st.session_state.show_follow_up = False
    if 'analysis_error' not in st.session_state:
        st.session_state.analysis_error = None
    if 'question_cache' not in st.session_state:
        st.session_state.question_cache = {}

    # Sidebar for company info and controls
    with st.sidebar:
        st.header("Company Information")
        with st.form("company_info_form"):
            company_name = st.text_input("Company Name", placeholder="e.g., TechCorp")
            industry = st.text_input("Industry", placeholder="e.g., Technology")
            size = st.text_input("Size (e.g., employees)", placeholder="e.g., 500")
            company_description = st.text_area("Company Description", placeholder="Describe your company...")
            if st.form_submit_button("Submit"):
                if company_name and industry:
                    new_company_info = normalize_company_info({
                        "name": company_name,
                        "industry": industry,
                        "size": size,
                        "description": company_description
                    })
                    if new_company_info != st.session_state.company_info:
                        logging.info(f"Company info changed: {new_company_info}")
                        st.session_state.company_info = new_company_info
                        st.session_state.last_company_info = new_company_info.copy()
                        st.session_state.selected_task = None
                        st.session_state.current_questions = []
                        st.session_state.answers = []
                        st.session_state.question_phase = True
                        st.session_state.questions_asked = 0
                        st.session_state.final_response_generated = False
                        st.session_state.follow_up_count = 0
                        st.session_state.ratings = {}
                        st.session_state.show_follow_up = False
                        st.session_state.question_cache = {}
                        st.session_state.analysis_error = None
                        st.success("Company information saved!")
                        st.rerun()
                else:
                    st.error("Please provide at least Company Name and Industry.")

        st.header("Task Selection")
        selected_task = st.selectbox("Choose a Task", [""] + list(AGENT_CLASSES.keys()))
        if selected_task and selected_task != st.session_state.selected_task:
            logging.info(f"Task changed to: {selected_task}")
            st.session_state.selected_task = selected_task
            st.session_state.conversation = []
            st.session_state.agent = AGENT_CLASSES[selected_task](model)
            st.session_state.current_questions = []
            st.session_state.answers = []
            st.session_state.question_phase = True
            st.session_state.questions_asked = 0
            st.session_state.final_response_generated = False
            st.session_state.follow_up_count = 0
            st.session_state.ratings = {}
            st.session_state.show_follow_up = False
            st.session_state.last_task = selected_task
            st.session_state.analysis_error = None
            st.rerun()

        if (
            selected_task
            and st.session_state.selected_task
            and st.session_state.company_info
            and not st.session_state.current_questions
        ):
            cache_key = f"{selected_task}_{json.dumps(normalize_company_info(st.session_state.company_info), sort_keys=True)}"
            if cache_key in st.session_state.question_cache:
                logging.info(f"Cache hit for key: {cache_key}")
                st.session_state.current_questions = st.session_state.question_cache[cache_key]
            else:
                logging.info(f"Cache miss for key: {cache_key}, generating questions")
                questions = generate_task_questions(selected_task, st.session_state.company_info)
                st.session_state.question_cache[cache_key] = questions
                st.session_state.current_questions = questions

        if st.button("Clear History"):
            logging.info("Clearing history")
            st.session_state.conversation = []
            st.session_state.agent = None
            st.session_state.selected_task = None
            st.session_state.question_phase = True
            st.session_state.questions_asked = 0
            st.session_state.current_questions = []
            st.session_state.answers = []
            st.session_state.final_response_generated = False
            st.session_state.follow_up_count = 0
            st.session_state.ratings = {}
            st.session_state.show_follow_up = False
            st.session_state.last_task = None
            st.session_state.api_call_count = 0
            st.session_state.question_cache = {}
            st.session_state.analysis_error = None
            st.rerun()
        if st.session_state.conversation:
            chat_json = json.dumps(st.session_state.conversation, indent=2)
            st.download_button("Download Chat History", chat_json, "chat_history.json", "application/json")

    # Main chat interface
    if st.session_state.company_info and st.session_state.selected_task and st.session_state.current_questions:
        st.subheader(f"Task: {st.session_state.selected_task}")
        # Progress bar
        total_steps = max(len(st.session_state.current_questions), 7) + 1 + st.session_state.max_follow_ups
        current_progress = st.session_state.questions_asked + (1 if st.session_state.final_response_generated else 0) + st.session_state.follow_up_count
        progress = min(current_progress / total_steps, 1.0)
        st.progress(progress, text=f"Step {current_progress} of {total_steps}")

        # Chat display
        for idx, message in enumerate(st.session_state.conversation):
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
                if message["role"] == "assistant" and message.get("is_final_or_follow_up", False):
                    if idx not in st.session_state.ratings:
                        with st.form(key=f"rating_form_{idx}"):
                            rating = st.slider("Rate this response", 1, 5, 3, key=f"rating_{idx}")
                            if st.form_submit_button("Submit Rating"):
                                st.session_state.ratings[idx] = rating
                                if idx == len(st.session_state.conversation) - 1 and not st.session_state.show_follow_up:
                                    st.session_state.show_follow_up = True
                                st.rerun()
                    else:
                        st.write(f"Rating: {st.session_state.ratings[idx]} / 5")

        # Question phase
        if st.session_state.question_phase and st.session_state.questions_asked < len(st.session_state.current_questions):
            question = st.session_state.current_questions[st.session_state.questions_asked]
            with st.chat_message("assistant", avatar="🤖"):
                with st.form(key=f"question_form_{st.session_state.questions_asked}"):
                    st.markdown(question["question"])
                    if question["type"] in ["MCQ", "Radio"]:
                        answer = st.selectbox("Choose an option", question["options"], key=f"select_{st.session_state.questions_asked}")
                    else:  # Input
                        answer = st.text_input("Your answer", key=f"input_{st.session_state.questions_asked}")
                    if st.form_submit_button("Submit"):
                        if answer or question["type"] in ["MCQ", "Radio"]:
                            st.session_state.conversation.append({"role": "assistant", "content": question["question"]})
                            st.session_state.conversation.append({"role": "user", "content": answer})
                            st.session_state.answers.append({
                                "question": question["question"],
                                "answer": answer,
                                "type": question["type"]
                            })
                            st.session_state.questions_asked += 1
                            if st.session_state.questions_asked >= len(st.session_state.current_questions):
                                st.session_state.question_phase = False
                                logging.info("All questions answered, proceeding to analysis")
                            st.rerun()
                        else:
                            st.error("Please provide an answer.")

        # Generate final response
        elif not st.session_state.question_phase and not st.session_state.final_response_generated:
            with st.spinner("Generating detailed analysis..."):
                try:
                    company_info_str = ", ".join(f"{k}: {v}" for k, v in st.session_state.company_info.items() if v)
                    answers_str = json.dumps(st.session_state.answers, indent=2)
                    history = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.conversation)
                    
                    response = st.session_state.agent.generate_final_response(history, company_info_str, answers_str)
                    increment_api_call()
                    logging.info(f"Final Analysis Response:\n{response}")

                    # Store and display response
                    st.session_state.conversation.append({
                        "role": "assistant",
                        "content": response,
                        "is_final_or_follow_up": True
                    })
                    st.session_state.final_response_generated = True

                    # Display analysis in a new section
                    with st.container():
                        st.header("Analysis Results")
                        st.markdown(f"### {st.session_state.selected_task} Analysis")
                        st.markdown(response)

                except Exception as e:
                    error_msg = f"Failed to generate analysis: {str(e)}"
                    logging.error(error_msg)
                    st.session_state.analysis_error = error_msg
                    st.error("An error occurred while generating the analysis. Please try again or check the logs.")
                
                st.rerun()

        # Display analysis error if present
        if st.session_state.analysis_error:
            st.error(st.session_state.analysis_error)

        # Follow-up phase
        elif st.session_state.final_response_generated and st.session_state.follow_up_count < st.session_state.max_follow_ups and st.session_state.show_follow_up:
            user_input = st.chat_input("Ask a follow-up question or provide feedback...")
            if user_input:
                try:
                    st.session_state.conversation.append({"role": "user", "content": user_input})
                    st.session_state.follow_up_count += 1
                    with st.spinner("Processing follow-up..."):
                        company_info_str = ", ".join(f"{k}: {v}" for k, v in st.session_state.company_info.items() if v)
                        history = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.conversation)
                        response = st.session_state.agent.generate_follow_up_response(history, company_info_str, user_input)
                        increment_api_call()
                        logging.info(f"Follow-up Response:\n{response}")
                        st.session_state.conversation.append({
                            "role": "assistant",
                            "content": response,
                            "is_final_or_follow_up": True
                        })
                except Exception as e:
                    logging.error(f"Failed to generate follow-up response: {str(e)}")
                    st.error("Error processing follow-up. Please try again.")
                st.rerun()

if __name__ == "__main__":
    main()
