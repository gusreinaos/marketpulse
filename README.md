# MarketPulse

### :bulb: <ins>What is this? </ins>
MarketPulse is a group project for the Software Engineering for DIT826 Software Engineering for Data-Intensive AI Applications where we designed a platform  to give analysis of current market trends for traded NASDAQ companies. By using Machine Learning, we the public sentiment of a company, whether negative, neutral, or positive based on data collected from social media posts. 

To improve the accuracy of the results, we also integrate additional data such as inflation rates and the specific company stock prices. The platform is interactive and customizable, allowing users to adapt their experience. You can browse the most popular stocks, search for specific companies, and add favorites, ensuring you always have the information you need at your fingertips.

### 🧐 <ins>How does it work?</ins>

Our application uses two ML models: a sentiment analysis model and a market trend analysis model, that work together to give information into market trends based on public sentiment and financial data.

When a user makes a query on MarketPulse, the following steps are executed:

1. **User Query**: The user searches for a specific company's stock or browses popular stocks on the platform.
2. **Data Retrieval**: 
    - **Sentiment Analysis**: The system retrieves recent tweets related to the queried company.
    - **Financial Data**: Stock prices, GDP, and inflation rates are gathered from external sources like Yahoo Finance and FRED.
3. **Sentiment Model Processing**:
    - The sentiment analysis model processes the tweets to determine their sentiment (negative, neutral, or positive).
    - The results are averaged to obtain a daily sentiment score for the company.
4. **Market Model Processing**:
    - The daily sentiment scores, along with the financial data, are fed into the market trend analysis model.
    - This model predicts the market trend (downtrend, neutral, uptrend) for the queried company.
5. **Results Display**: The predicted market trend and relevant data are presented to the user in an interactive and customizable format, allowing them to view trends, search for specific stocks, and add favorites.

