# AI Business Analysis Platform 🚀

Welcome to the **AI Business Analysis Platform**, a cutting-edge Streamlit-powered web application that leverages Google’s Gemini AI to deliver actionable business insights! 📊 This platform is designed to help companies analyze strategic planning, organizational health, operational efficiency, and stakeholder engagement with a sleek, user-friendly interface. Whether you're a startup or an enterprise, unlock your business potential with AI-driven recommendations! 🌟

---

## ✨ Features

This platform is packed with powerful features to streamline your business analysis process:

- **Task-Driven Analysis** 🛠️
  - Choose from four specialized tasks: Strategic Planning, Organizational Assessment, Operational Efficiency Analysis, or Stakeholder Engagement Strategy.
  - Each task is powered by a dedicated AI agent tailored to deliver precise insights.

- **Interactive Company Input Form** 📝
  - Input company details (name, industry, size, description) and select a task in a single, intuitive sidebar form.
  - Submitting the form automatically triggers the analysis workflow, saving time and effort.

- **Dynamic Question Generation** ❓
  - Automatically generates up to 5 relevant questions (MCQ, Radio, or Input) based on the company and task.
  - Questions are cached to minimize API calls, ensuring efficiency and speed.

- **Comprehensive Analysis Report** 📑
  - After answering questions, receive a detailed 500–1000 word report in a dedicated "Analysis Report" section.
  - Structured with sections: Executive Summary, Company Context, Analysis of Responses, Strategic Recommendations, and Conclusion.
  - Download the report as a markdown file for easy sharing.

- **Concise Follow-Up Responses** 💬
  - Ask up to 5 follow-up questions in a chat-style interface, receiving short (50–100 word) actionable answers.
  - Rate responses (1–5 stars) to provide feedback on AI insights.

- **Enhanced UI with Custom Styling** 🎨
  - Modern, blue-themed design with custom CSS for a professional look:
    - Buttons, progress bars, and chat containers.
    - Clean layout with bordered sections, clear headers, and a responsive wide layout.
    - Styled progress bar tracks your analysis journey (questions, analysis, follow-ups).

- **Robust State Management** 🔄
  - Seamless transitions between phases: company input → questions → analysis → follow-ups.
  - Automatic progression to analysis after answering all questions, no manual button required.

- **Terminal Logging for Debugging** 🖥️
  - Detailed logs for:
    - Answer texts and categories (Positive, Negative, Neutral).
    - Categorized answers, final response (first 200 chars), and follow-up responses.
    - State transitions and API call counts.

- **Error Handling & Resilience** 🛡️
  - Graceful handling of API errors, JSON parsing issues, and question indexing problems.
  - User-friendly error messages and fallback questions ensure a smooth experience.

- **Downloadable History** 📥
  - Export the entire conversation history as a JSON file for record-keeping.

- **API Call Optimization** ⚡
  - Caches questions to reduce Gemini API calls, addressing rate limit concerns.
  - Tracks and displays API call count in the sidebar for transparency.

---

## 🛠️ Installation

Get started in just a few steps! Follow these instructions to set up the platform locally.

### Prerequisites
- Python 3.8+ 🐍
- Google Gemini API key (sign up at [Google AI Studio](https://aistudio.google.com/)) 🔑
- Git (optional, for cloning the repo) 🌐

### Steps
1. **Clone the Repository** 📂
   ```bash
   git clone https://github.com/your-repo/ai-business-analysis.git
   cd ai-business-analysis
   ```

2. **Install Dependencies** 📦
   ```bash
   pip install -r requirements.txt
   ```
   Ensure `requirements.txt` includes:
   ```
   streamlit==1.38.0
   google-generativeai==0.7.2
   python-dotenv==1.0.1
   ```

3. **Set Up Environment Variables** ⚙️
   - Create a `.env` file in the project root:
     ```bash
     touch .env
     ```
   - Add your Gemini API key:
     ```bash
     echo "GEMINI_API_KEY=your-api-key-here" >> .env
     ```

4. **Run the Application** 🚀
   ```bash
   streamlit run app.py
   ```
   Open your browser to `http://localhost:8501` to access the app! 🌐

---

## 📖 Usage

Here’s how to use the platform to analyze your business:

1. **Enter Company Details** 🏢
   - In the sidebar, fill out the form with your company’s name, industry, size, and description.
   - Select a task (e.g., Strategic Planning) from the dropdown.
   - Click **Submit** to start the analysis process. ✅

2. **Answer Questions** ❓
   - Answer up to 5 questions (MCQ, Radio, or Input) about your company.
   - Questions are tailored to the task and company context.
   - After the last question, the app automatically generates the analysis. ⏳

3. **View Analysis Report** 📊
   - A detailed 500–1000 word report appears in the "Analysis Report" section.
   - Structured with clear sections for easy reading.
   - Download the report as a markdown file with one click. 📥

4. **Ask Follow-Up Questions** 💬
   - In the "Follow-Up Questions" section, use the chat input to ask up to 5 follow-up questions.
   - Receive concise, actionable responses (50–100 words).
   - Rate each response to provide feedback. ⭐

5. **Clear or Download History** 🔄
   - Click **Clear Analysis** to start over with a new company or task.
   - Download the conversation history as a JSON file for records.

---

## 🐛 Debugging Tips

Encounter an issue? Here’s how to troubleshoot:

- **Questions Repeat** 🔁
  - Check terminal logs for `question_phase` and `questions_asked`.
  - Ensure `st.session_state.current_questions` isn’t empty (log it).
  - Clear analysis to reset state.

- **No Analysis Generated** 🚫
  - Verify `final_response=False` after the last question (add debug log).
  - Check for 429 API errors (rate limits) in logs.
  - Upgrade your Gemini API quota if needed.

- **Syntax Errors** 🛠️
  - Run `python -m py_compile app.py` to validate syntax.
  - Check for unclosed parentheses in prompts or expressions.

- **UI Issues** 🎨
  - Disable custom CSS temporarily to isolate styling problems.
  - Update Streamlit (`pip install -U streamlit`).

- **Logs** 📜
  - Enable verbose logging in `app.py` to trace state changes:
    ```python
    logging.info(f"State: {dict(st.session_state)}")
    ```

---

## 🛑 Known Limitations

- **Gemini API Dependency** 🌐
  - Requires a valid Gemini API key and internet connection.
  - Rate limits may apply; caching mitigates this.

- **Question Count** ❓
  - Limited to 5 questions per analysis for brevity.

- **Follow-Up Limit** 💬
  - Up to 5 follow-up questions to maintain focus.

- **Non-Latin Characters** 🈷️
  - UI and reports are optimized for Latin-based text. Non-Latin support may require additional font configurations.

---

## 🚀 Future Enhancements

We’re planning to make this platform even better! Here’s what’s on the horizon:

- **Multi-Language Support** 🌍: Add support for non-Latin languages with appropriate fonts.
- **Custom Question Count** ❓: Allow users to configure the number of questions.
- **Advanced Analytics** 📈: Integrate charts and visualizations in the analysis report.
- **Real-Time Collaboration** 👥: Enable team-based input and analysis sharing.
- **Offline Mode** 📴: Cache AI models for limited offline functionality.

---

## 🤝 Contributing

We welcome contributions to make this platform even better! 🎉

1. Fork the repository 🍴
2. Create a feature branch (`git checkout -b feature/awesome-feature`) 🌿
3. Commit your changes (`git commit -m "Add awesome feature"`) 💾
4. Push to the branch (`git push origin feature/awesome-feature`) 🚀
5. Open a Pull Request 📬

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) and report issues via [GitHub Issues](https://github.com/your-repo/ai-business-analysis/issues).

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 📜

---

## 🙌 Acknowledgments

- **Google Gemini AI** for powering the analysis engine 🤖
- **Streamlit** for the awesome web app framework 🌐
- **You**, for exploring this platform and unlocking business insights! 💼

---

**Ready to transform your business with AI?** Start analyzing today! 🚀