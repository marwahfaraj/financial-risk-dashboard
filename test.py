# # import mysql.connector
# # from dotenv import load_dotenv
# # import os

# # # Load environment variables
# # load_dotenv()

# # # Database connection details
# # DB_CONFIG = {
# #     "host": os.getenv("DB_HOST"),
# #     "user": os.getenv("DB_USER"),
# #     "password": os.getenv("DB_PASSWORD"),
# #     "database": os.getenv("DB_NAME")
# # }

# # # Test connection
# # try:
# #     connection = mysql.connector.connect(**DB_CONFIG)
# #     print("Connection successful!")
# # except Exception as e:
# #     print(f"Error connecting to database: {e}")
# # finally:
# #     if connection.is_connected():
# # #         connection.close()
# # import pandas as pd

# # df= pd.read_csv('/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/data/processed/combined_stock_metrics.csv')
# # print(df.columns)

# # import pandas as pd

# # # Load the consumer complaints dataset
# # file_path = "/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/data/raw/complaints.csv"
# # data = pd.read_csv(file_path, low_memory=False)

# # # Convert company names to lowercase for uniformity
# # data["Company"] = data["Company"].str.lower()

# # # Check if there are complaints about Apple or Meta
# # apple_complaints = data[data["Company"].str.contains("apple", na=False, case=False)]
# # meta_complaints = data[data["Company"].str.contains("meta|facebook", na=False, case=False)]

# # # Display the number of complaints found
# # len_apple = len(apple_complaints)
# # len_meta = len(meta_complaints)

# # print(apple_complaints['Company'].value_counts(), meta_complaints['Company'].value_counts())

# # import openai
# # import os
# # from dotenv import load_dotenv
# # from openai import OpenAIError


# # # Load environment variables
# # load_dotenv()

# # # Retrieve the API key from .env file
# # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # if not OPENAI_API_KEY:
# #     print("❌ No API key found. Please add 'OPENAI_API_KEY' to your .env file.")
# # else:
# #     openai.api_key = OPENAI_API_KEY
# #     try:
# #         # Make a test request to verify the key
# #         models = openai.Client(api_key=OPENAI_API_KEY).models.list()
# #         print("✅ API key is valid! Available models:")
# #         for model in models['data']:
# #             print(f"- {model['id']}")
# #     except openai.error.AuthenticationError:
# #         print("❌ Invalid API key. Please check your key and try again.")
# #     except Exception as e:
# #         print(f"⚠️ Error: {str(e)}")

# import streamlit as st
# import time
# import streamlit.components.v1 as components
# from phi.agent import Agent
# from phi.model.openai import OpenAIChat
# from phi.tools.yfinance import YFinanceTools
# from dotenv import load_dotenv
# import os

# # ---- 🔑 Load Environment Variables & API Key ----
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if not OPENAI_API_KEY:
#     st.error("⚠️ OpenAI API key is missing! Please add it to the `.env` file.")
#     st.stop()

# # ---- 🧠 Initialize Financial AI Agent ----
# finance_agent = Agent(
#     name="Finance AI Agent",
#     model=OpenAIChat(id="gpt-4o", api_key=OPENAI_API_KEY),
#     tools=[
#         YFinanceTools(
#             stock_price=True,
#             analyst_recommendations=True,
#             stock_fundamentals=True,
#             company_news=True
#         )
#     ],
#     instructions=[
#         "Respond with concise financial insights.",
#         "Display data in markdown tables when applicable.",
#         "If no data is available, inform the user politely."
#     ],
#     show_tool_calls=True,
#     markdown=True,
# )

# # ---- 🎨 Streamlit Page Configuration ----
# st.set_page_config(page_title="📈 Financial Dashboard", layout="wide")

# # ---- 📌 Welcome Message ----
# st.title("📈 Financial Market & Prediction Dashboard")
# st.markdown("""
# Welcome to the **Financial Market & Prediction Dashboard**!  
# Explore real-time stock insights, model performance, and interactive data visualizations.  
# Use the **navigation menu on the left** to explore different sections.
# """)

# # ---- 🔘 Navigation Menu ----
# menu = ["📊 Financial Stock Analysis", "📈 ElasticNet Model Performance", "🤖 Financial AI Assistant"]
# choice = st.sidebar.radio("🔎 Select View", menu)

# # ---- 📊 Financial Stock Analysis Dashboard ----
# if choice == "📊 Financial Stock Analysis":
#     st.header("📊 Financial Stock Analysis")
#     st.markdown("""
# This section provides **detailed stock analysis**, including:
# - 📈 Stock price trends  
# - 📊 Market volatility  
# - 🏛️ Company fundamentals & news  
# """)

#     components.html(
#         """
#         <div class='tableauPlaceholder' id='viz1739859015908' style='position: relative'>
#             <noscript><a href='#'><img alt='Dashboard 1 ' src='https://public.tableau.com/static/images/fi/financial_stock_analysis/Dashboard1/1_rss.png' style='border: none' /></a></noscript>
#             <object class='tableauViz'  style='display:none;'>
#                 <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
#                 <param name='embed_code_version' value='3' /> 
#                 <param name='name' value='financial_stock_analysis/Dashboard1' />
#                 <param name='tabs' value='no' />
#                 <param name='toolbar' value='yes' />
#                 <param name='static_image' value='https://public.tableau.com/static/images/fi/financial_stock_analysis/Dashboard1/1.png' /> 
#                 <param name='animate_transition' value='yes' />
#                 <param name='display_static_image' value='yes' />
#                 <param name='display_spinner' value='yes' />
#                 <param name='display_overlay' value='yes' />
#                 <param name='display_count' value='yes' />
#                 <param name='language' value='en-US' />
#             </object>
#         </div>                
#         <script type='text/javascript'>                    
#             var divElement = document.getElementById('viz1739859015908');                    
#             var vizElement = divElement.getElementsByTagName('object')[0];                    
#             if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} 
#             else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} 
#             else { vizElement.style.width='100%';vizElement.style.height='1377px';}                     
#             var scriptElement = document.createElement('script');                    
#             scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
#             vizElement.parentNode.insertBefore(scriptElement, vizElement);                
#         </script>
#         """,
#         height=820,
#     )

# # ---- 📈 ElasticNet Model Performance Dashboard ----
# elif choice == "📈 ElasticNet Model Performance":
#     st.header("📈 ElasticNet Model Performance")
#     st.markdown("""
# This section showcases the **ElasticNet Regression Model's performance** in predicting stock returns (ROI).  
# Key insights include:
# - ✅ Actual vs. Predicted ROI  
# - ❌ Prediction Errors  
# - 📊 Model Performance Metrics (R², RMSE)  
# """)

#     components.html(
#         """
#         <div class='tableauPlaceholder' id='viz1739858850633' style='position: relative'>
#             <noscript><a href='#'><img alt='Dashboard 2 ' src='https://public.tableau.com/static/images/El/ElasticNetModelPerformance/Dashboard2/1_rss.png' style='border: none' /></a></noscript>
#             <object class='tableauViz'  style='display:none;'>
#                 <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
#                 <param name='embed_code_version' value='3' /> 
#                 <param name='name' value='ElasticNetModelPerformance/Dashboard2' />
#                 <param name='tabs' value='no' />
#                 <param name='toolbar' value='yes' />
#                 <param name='static_image' value='https://public.tableau.com/static/images/El/ElasticNetModelPerformance/Dashboard2/1.png' /> 
#                 <param name='animate_transition' value='yes' />
#                 <param name='display_static_image' value='yes' />
#                 <param name='display_spinner' value='yes' />
#                 <param name='display_overlay' value='yes' />
#                 <param name='display_count' value='yes' />
#                 <param name='language' value='en-US' />
#             </object>
#         </div>                
#         <script type='text/javascript'>                    
#             var divElement = document.getElementById('viz1739858850633');                    
#             var vizElement = divElement.getElementsByTagName('object')[0];                    
#             if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} 
#             else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} 
#             else { vizElement.style.width='100%';vizElement.style.height='777px';}                     
#             var scriptElement = document.createElement('script');                    
#             scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
#             vizElement.parentNode.insertBefore(scriptElement, vizElement);                
#         </script>
#         """,
#         height=820,
#     )

# # ---- 🤖 Financial AI Assistant with Mocked Responses and Delay ----
# elif choice == "🤖 Financial AI Assistant":
#     st.header("🤖 Financial AI Assistant")
#     st.markdown("""
# Ask the assistant about **real-time stock data**, **market trends**, or **financial insights**.  
# Example questions:  
# - *What is the current stock price of Google (GOOGL)?*  
# - *Get me the latest news about Apple (AAPL).*  
# - *What are the fundamentals of Tesla?*  
# """)

#     mocked_responses = {
#         "What is the current stock price of Google (GOOGL)?": """
#         **Current Stock Price of GOOGL**  
#         | Date       | Open  | High  | Low   | Close  | Volume     |
#         |------------|-------|-------|-------|--------|------------|
#         | 2025-02-19 | 145.2 | 147.0 | 144.5 | 146.3  | 1,250,000  |
#         """,

#         "Get me the latest news about Apple (AAPL).": """
#         **Latest News about Apple (AAPL)**  
#         - 📰 *Apple Reports Record Q1 Earnings* - Bloomberg (2025-02-18)  
#         - 📰 *Apple Expands into AI Sector* - CNBC (2025-02-17)  
#         - 📰 *New iPhone Release Gains Positive Reviews* - TechCrunch (2025-02-16)  
#         """,

#         "What are the fundamentals of Tesla?": """
#         **Tesla Fundamentals**  
#         | Metric              | Value     |
#         |---------------------|-----------|
#         | Market Cap          | $800B     |
#         | P/E Ratio           | 52.4      |
#         | EPS                 | $5.67     |
#         | Dividend Yield      | 0.00%     |
#         | Revenue (TTM)       | $85.0B    |
#         | Profit Margin       | 12.5%     |
#         """
#     }

#     user_input = st.text_input("💬 Enter your financial question:")

#     if st.button("🔎 Get Insights"):
#         if user_input.strip():
#             with st.spinner("Fetching data... Please wait ⏳"):
#                 time.sleep(3)  # ⏳ Add delay (3 seconds) for realism
#                 if user_input in mocked_responses:
#                     st.markdown(mocked_responses[user_input], unsafe_allow_html=True)
#                 else:
#                     try:
#                         response = finance_agent.run(user_input)
#                         final_response = getattr(response, "content", None) or response.get("content", "⚠️ No data received.")
#                         st.markdown(final_response, unsafe_allow_html=True)
#                     except Exception as e:
#                         st.error(f"❌ Could not fetch data: {str(e)}")
#         else:
#             st.warning("⚠️ Please enter a valid question!")

import os

print("Processed Data Path:", processed_file_path)
print("Files in directory:", os.listdir(os.path.dirname(processed_file_path)))
