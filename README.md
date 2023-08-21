# Stock prediction (using FinGPT and FinRL) assisstant Project 


## Machine Learning Enginnering is 10% of Machine Learning, and 90% of Enginnering.

  When I First heard this, I am astonished, almost stun. For that all the way in the colleage, we have been learning the Machine learning the way that how we manupulate the data adn Algorithm to let the computer "think", but in fact, making a good application is not just having the best data, the efficient Algorithm. It is always the Enginnering, the trade off, the big effort to make the new function up and running online. 

## Hight level design of Pipeline and data flywheel 



## I am going to redo the app with the new idea of using FinGPT (for sentiment analysis) and FinRL Meta (for batch data training)


### 1. Problem Understanding and Definition

#### Objective:
- **Document**:  Problem Statement document.
  - Define the exact stock indices or companies you're focusing on.
    for the POV, will focusing on a couples of company

  - Outline the prediction horizon (e.g., daily, weekly).
    Intraday is very good start point for the real time data project. I will set the getting data in 5 mins. 

#### Significance and Impact:
- Investment assisting is always a hit of the market. 
- Identify potential financial metrics to quantify the impact (e.g., ROI).



---

### 2. Data Collection and Exploration

#### Data Sources:
- API, article scrapping, official documents, sec, earnings transcripts, etc. 

#### Data Gathering:
- **Code**: Write ETL (Extract, Transform, Load) scripts to collect data. (We are using AWS)
- **Database**: Store the raw data in a scalable database like AWS RDS Database. 

- <img width="1581" alt="Screenshot 2023-08-21 at 12 54 05" src="https://github.com/dada325/stock_prediction_app/assets/7775973/4a36a1d3-9c8b-489b-85fc-537a7d9136d4">
Two Lambda functions, one to get 


-  **Lambda Functions for New Features**
**SEC Filings**
Create a new Lambda function (fetch_sec_filings) that pulls SEC Filings for a list of companies.
Store this data in the corresponding table in your PostgreSQL database.
**Earnings Transcripts**
Create another Lambda function (fetch_earnings_transcripts) to pull Earnings Transcripts.
Store this data in the corresponding table in your PostgreSQL database.
**Relevant News Articles**
Create a Lambda function (fetch_news_articles) to pull in news articles relevant to the stock market.
Store this data in the corresponding table in your PostgreSQL database.

- Texts data:


#### SEC Filings

1. **Source**: SEC provides a public API where you can fetch filings.
2. **Storage**: Store the raw filings in a structured format in your PostgreSQL database or in a Data Lake like AWS S3.
3. **Lambda Function**: Create a Lambda function (`fetch_sec_filings`) to periodically pull this data.

#### Earnings Transcripts

1. **Source**: Several financial news websites and APIs provide earnings transcripts.
2. **Storage**: Due to the textual nature of transcripts, you may also consider text search optimized storage like Elasticsearch, in addition to PostgreSQL.
3. **Lambda Function**: Create a Lambda function (`fetch_earnings_transcripts`) to regularly update this information.

#### Relevant News Articles

1. **Source**: You can use APIs from news aggregators or trusted financial news websites.
2. **Storage**: AWS S3 can be a good option for storing large volumes of news articles, especially if they contain multimedia elements.
3. **Lambda Function**: Use a Lambda function (`fetch_news_articles`) to pull this data.


**Data Transformation**: Depending on the source, you may need to transform the data before storing it in a way that's useful for your application.

**Security**: Secure your data both in transit and at rest. Given that financial data is sensitive, employ best practices to keep it secure.

Given that potentially large and diverse sets of data, AWS's robust cloud storage and compute options are a good fit. Lambda functions are a cost-effective way to collect data at scale without maintaining a running server.







#### Initial Exploration:
- **Quality Check**: Implement automated checks for missing values and anomalies.



---

### 3. Data Preprocessing

#### Missing Values:
- Implement imputation algorithms tailored for time-series data, like forward-fill or interpolation.

#### Outliers:
- Use Z-score or Tukey's method to identify outliers and replace them.

#### Data Transformation:
- Use Min-Max scaling or Z-score normalization.



---


### 4. Feature Engineering

#### Technical Indicators:
- Calculate technical indicators like SMA, EMA, RSI, and MACD.
  
#### Market Indicators:
- Add features like market sentiment, news sentiment, or S&P 500 performance.

#### Feature Selection:
- Run algorithms like Recursive Feature Elimination (RFE).

#### Deliverables:
- Feature Engineering code repository.
- Dataset with engineered features stored in a database.

---

### 5. Exploratory Data Analysis (EDA)


#### Visualizations:
- Generate interactive dashboards using tools like Tableau or Power BI.
  
#### Correlations:
- Compute Spearman and Pearson correlation coefficients for all features.

#### Deliverables:
- EDA Dashboard.
- EDA report.

---

### 6. Model Selection and Training

#### numerical data will be go to the Time series + Deep Reinforcement learning (PPO) pipe line 
#### Algorithm Selection:(for structure data)
- Conduct literature reviews or pilot studies to select algorithms.

#### Data Split:
- Use Walk-Forward Validation or Time Series Split for more accurate evaluation.

#### Backtesting:
- Develop a backtesting engine to simulate trades and calculate performance metrics like Sharpe ratio.

#### Model Training and Tuning:
- Use hyperparameter tuning libraries like Optuna or Hyperopt.

#### Evaluation:
- Calculate error metrics (e.g., RMSE, MAE) and financial metrics (e.g., ROI from backtesting).

### For the Text data: 

#### Llama2 model fine tuning for the financial document. (or using FinGPT + FinRL meta, for that training a Llama2 7b is costing a lot. )

#### Prompt Engineering: 
- for the output to the user, will merge the numerical data and the prediction base on the SEC Filings , Earnings Transcripts, and some scraped article on the web.
- Output format is dialoug respond to the user question.



---

### Second Phase:

#### Deployment:
- Use Docker containers or cloud services  AWS SageMaker for deployment.

#### Monitoring and Maintenance:
- Implement automated monitoring using Grafana or custom dashboards.
- Schedule periodic retraining of the model.

#### Do not need user feedback. 
  

### 1. Web App Development Process:

Once you have a trained agent, you can integrate it into a web app for user interaction. Here's a general workflow:

#### a. **Backend Development**:
- **Model Serving**: Use FastAPI to serve the trained model. The backend will handle requests to get trading actions based on the latest data.
- **Data Streaming**: Integrate with a real-time data provider to get live stock prices. This can be done using websockets or RESTful APIs, depending on the data source.

#### b. **Frontend Development**:
- Develop a user interface using a framework like React. 
- Display real-time stock prices and the trading actions recommended by the RL agent.
- Optionally, show historical performance metrics, charts, and other relevant information.

#### c. **Deploying the App**:
- Use   AWS to deploy backend.
- Use services Vercel for the frontend.

#### d. **Continuous Monitoring & Retraining**:
- Continuously monitor the agent's performance. If the strategy starts underperforming, consider retraining the agent with newer data.
- Ensure the app handles errors gracefully, especially when dealing with live financial data and trading decisions.


### 2. Monitoring and Maintenance:



### Important Points:

- **User Safety**: Always include disclaimers stating that the trading strategy is based on simulations and past performance is not indicative of future results. It's essential to ensure users are aware of the risks.
  
- **Testing**: Before deploying, rigorously test the app in a sandbox or simulated environment. Financial applications can have significant repercussions if there's a bug.

- **Security**: Given that you're dealing with financial data, ensure that the app is secure. Use HTTPS, secure any databases or data storage, and regularly update and patch your systems.

Remember, while FinRL provides tools to develop and train RL-based trading strategies, deploying them in a real-world scenario requires careful consideration and thorough testing.
