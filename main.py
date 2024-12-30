import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
import os

# Set page configuration
st.set_page_config(
    page_title="Smart Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for colorful UI
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .stSelectbox>div>div>input {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=['Date', 'Category', 'Amount', 'Description']
    )

def format_currency(amount):
    """Format amount in Indian Rupees"""
    return f"₹{amount:,.2f}"

def get_ai_advice(expenses_df, groq_chat):
    """Get AI-powered financial advice based on expense patterns"""
    if len(expenses_df) == 0:
        return "Start adding your expenses to get personalized advice!"

    # Prepare expense summary for AI
    total_spent = expenses_df['Amount'].sum()
    category_totals = expenses_df.groupby('Category')['Amount'].sum()
    highest_category = category_totals.idxmax()
    
    prompt = f"""
    Based on the following expense data in Indian Rupees (INR):
    Total spent: ₹{total_spent:.2f}
    Highest spending category: {highest_category} (₹{category_totals[highest_category]:.2f})
    Category breakdown: {category_totals.to_dict()}
    
    Provide 3 specific, actionable financial advice points to help save money in the Indian context.
    Consider Indian lifestyle and spending patterns in your advice.
    """
    
    system_prompt = "You are a financial advisor providing concise, practical advice for Indian consumers."
    memory = ConversationBufferWindowMemory(k=3, memory_key="chat_history", return_messages=True)
    
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessagePromptTemplate.from_template("{human_input}")
    ])
    
    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt_template,
        verbose=False,
        memory=memory,
    )
    
    response = conversation.predict(human_input=prompt)
    return response

def main():
    # Header
    st.title("💰 Smart Personal Expense Tracker")
    st.markdown("---")

    # Initialize Groq
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name='llama3-8b-8192')
    else:
        st.warning("Please set the GROQ_API_KEY environment variable for AI advice.")
        groq_chat = None

    # Sidebar for adding expenses
    with st.sidebar:
        st.header("Add New Expense")
        date = st.date_input("Date", datetime.now())
        category = st.selectbox(
            "Category",
            ["Food & Dining", "Transportation", "Housing", "Utilities", "Entertainment", 
             "Shopping", "Healthcare", "Education", "Groceries", "Mobile & Internet",
             "Insurance", "Investment", "Other"]
        )
        amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
        description = st.text_input("Description")
        
        if st.button("Add Expense"):
            new_expense = pd.DataFrame({
                'Date': [date],
                'Category': [category],
                'Amount': [amount],
                'Description': [description]
            })
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
            st.success("Expense added successfully!")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Expense Summary")
        if not st.session_state.expenses.empty:
            total_expenses = st.session_state.expenses['Amount'].sum()
            st.metric("Total Expenses", format_currency(total_expenses))

            # Category-wise pie chart using Plotly
            fig_pie = px.pie(
                st.session_state.expenses,
                values='Amount',
                names='Category',
                title='Expenses by Category',
                hole=0.3
            )
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie)

    with col2:
        st.subheader("📈 Expense Trends")
        if not st.session_state.expenses.empty:
            # Time series chart using Plotly
            daily_expenses = st.session_state.expenses.groupby('Date')['Amount'].sum().reset_index()
            fig_line = px.line(
                daily_expenses,
                x='Date',
                y='Amount',
                title='Daily Expense Trend'
            )
            fig_line.update_layout(yaxis_title="Amount (₹)")
            st.plotly_chart(fig_line)

    # Display expense table
    st.subheader("📝 Expense Records")
    if not st.session_state.expenses.empty:
        # Create a copy of the dataframe with formatted currency
        display_df = st.session_state.expenses.copy()
        display_df['Amount'] = display_df['Amount'].apply(format_currency)
        st.dataframe(
            display_df.sort_values('Date', ascending=False),
            use_container_width=True
        )
    else:
        st.info("No expenses recorded yet. Start by adding an expense!")

    # Category-wise Analysis
    if not st.session_state.expenses.empty:
        st.subheader("📊 Category-wise Analysis")
        category_analysis = st.session_state.expenses.groupby('Category')['Amount'].agg(['sum', 'mean', 'count']).round(2)
        category_analysis.columns = ['Total Amount', 'Average Amount', 'Number of Transactions']
        category_analysis['Total Amount'] = category_analysis['Total Amount'].apply(format_currency)
        category_analysis['Average Amount'] = category_analysis['Average Amount'].apply(format_currency)
        st.dataframe(category_analysis, use_container_width=True)

    # AI Advice Section
    st.subheader("🤖 AI Financial Advice")
    if groq_chat and not st.session_state.expenses.empty:
        advice = get_ai_advice(st.session_state.expenses, groq_chat)
        st.info(advice)
    elif not groq_chat:
        st.warning("AI advice is not available without the Groq API key.")
    else:
        st.info("Add some expenses to get personalized AI advice!")

    # Export functionality
    if not st.session_state.expenses.empty:
        st.download_button(
            label="Download Expense Report",
            data=st.session_state.expenses.to_csv(index=False),
            file_name="expense_report.csv",
            mime="text/csv"
        )

    # Footer with monthly summary
    if not st.session_state.expenses.empty:
        st.markdown("---")
        st.subheader("📅 Monthly Summary")
        monthly_expenses = st.session_state.expenses.copy()
        # Convert Date column to datetime if it's not already
        monthly_expenses['Date'] = pd.to_datetime(monthly_expenses['Date'])
        monthly_expenses['Month'] = monthly_expenses['Date'].dt.strftime('%B %Y')
        monthly_summary = monthly_expenses.groupby('Month')['Amount'].sum().sort_index(ascending=False)
        
        for month, amount in monthly_summary.items():
            st.metric(month, format_currency(amount))

if __name__ == "__main__":
    main()
