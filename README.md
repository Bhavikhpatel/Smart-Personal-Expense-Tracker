# Smart Personal Expense Tracker
An intelligent personal finance application built with Streamlit that helps you track your expenses, visualize your spending patterns, and receive personalized financial advice powered by AI.

---

## ✨ Features

-   **Add Expenses:** Easily log your daily expenditures with details like category, amount (₹), and a short description.
-   **Interactive Dashboard:** Visualize your financial data with an intuitive and colorful dashboard.
-   **Expense Summary:** Get a quick overview of your total spending with a prominent metric.
-   **Categorical Analysis:** Understand where your money goes with an interactive pie chart breakdown by category.
-   **Trend Analysis:** Track your spending over time with a daily expense trend line chart.
-   **Detailed Records:** View, sort, and manage all your expense entries in a clean, filterable table.
-   **AI Financial Advisor:** Receive actionable, context-aware financial advice tailored to your spending habits in the Indian context, powered by **Groq** and **Llama3**.
-   **Data Export:** Download your complete expense report as a CSV file for offline analysis or record-keeping.
-   **Monthly Summary:** See a breakdown of your total expenses for each month.

---

## 🛠️ Tech Stack

-   **Framework:** [Streamlit](https://streamlit.io/)
-   **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
-   **Visualization:** [Plotly Express](https://plotly.com/python/plotly-express/)
-   **AI Integration:** [LangChain](https://www.langchain.com/) & [LangChain-Groq](https://python.langchain.com/docs/integrations/chat/groq/)
-   **LLM Provider:** [Groq](https://groq.com/) (using the `llama3-8b-8192` model)

---

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

-   Python 3.8+
-   A free API key from [Groq](https://console.groq.com/keys)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <url>
    cd smart-personal-expense-tracker
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    Create a `requirements.txt` file with the following content:
    ```txt
    streamlit
    pandas
    plotly
    langchain
    langchain-core
    langchain-groq
    ```
    Then, install the packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    The application requires a Groq API key for the AI features. Set this key as an environment variable in your system.

    **For Unix/macOS:**
    ```bash
    export GROQ_API_KEY="your_groq_api_key_here"
    ```

    **For Windows (Command Prompt):**
    ```bash
    set GROQ_API_KEY="your_groq_api_key_here"
    ```

    **For Windows (PowerShell):**
    ```bash
    $env:GROQ_API_KEY="your_groq_api_key_here"
    ```
    > **Note:** For a more permanent solution, add the environment variable to your system's settings or your shell's profile file (e.g., `.bashrc`, `.zshrc`).

### Running the Application

1.  Make sure your virtual environment is activated and the environment variable is set.
2.  Run the Streamlit application from the project's root directory:
    ```bash
    streamlit run app.py 
    ```
    *(Replace `app.py` with the name of your Python script if it's different.)*

3.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

---

## 📖 How to Use

1.  **Add an Expense:** Use the sidebar on the left to enter the details of a new expense (date, category, amount, description).
2.  **Submit:** Click the "Add Expense" button to log the entry.
3.  **View Dashboard:** The main dashboard will automatically update to reflect the new data.
4.  **Get AI Advice:** As you add more expenses, the "AI Financial Advice" section will provide personalized tips based on your spending patterns.
5.  **Download Report:** Click the "Download Expense Report" button at the bottom to save all your data to a `expense_report.csv` file.

---
