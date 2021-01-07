import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sklearn
from sklearn.decomposition import TruncatedSVD

st.markdown("<h1 style='text-align: left; color: red;'>TRENDING NOW</h1>", unsafe_allow_html=True)
st.sidebar.title("Welcome to Beauty Product Recommender System")

amazon_ratings = pd.read_csv('filtered_ratings_Beauty.csv')

popular_products = pd.DataFrame(amazon_ratings.groupby('ProductId')['Rating'].count())
popular_products['Avg_Rating'] = pd.DataFrame(amazon_ratings.groupby('ProductId')['Rating'].mean())
most_popular = popular_products.sort_values('Rating', ascending = False).head(10)
most_popular.columns = ['Number of Ratings','Average Ratings']
most_popular = most_popular.reset_index()

top1 = most_popular.iloc[0,0]
recommender = ['Type 1 (Rating Prediction)', 'Type 2 (Product Similarity)']

st.markdown("""Popular Products!""")

popular_graph = px.bar(most_popular, x='Number of Ratings',y='ProductId',orientation='h',color='Average Ratings')
st.plotly_chart(popular_graph)

ratings_utility_matrix = amazon_ratings.pivot_table(values='Rating', index='UserId', columns='ProductId', fill_value=0)
X = ratings_utility_matrix.T
user_Selection_list = list(ratings_utility_matrix.index)
product_Selection_list = list(X.index)


selected_recommender = st.selectbox("Other Recommendation",recommender)

#TYPE 1

selected_user = st.sidebar.selectbox("Please Choose Your Username:",user_Selection_list)

user_id = selected_user
st.sidebar.subheader("You are now Signed In as")
st.sidebar.success(user_id)
st.markdown("<h3 style='text-align: left; color: blue;'>SPECIAL FOR YOU</h3>", unsafe_allow_html=True)

recommender_result = pd.read_csv('Recommender Predictions.csv')
recommender_result = recommender_result.set_index('UserId')
def get_predictions(user_id, dataset):
    results = dataset.loc[user_id]
    return results


#TYPE 2

selected_product = st.sidebar.selectbox("Please Choose Your Product:",product_Selection_list)

SVD = TruncatedSVD(n_components=10)
decomposed_matrix = SVD.fit_transform(X)
correlation_matrix = np.corrcoef(decomposed_matrix)

i = selected_product

product_names = list(X.index)
product_ID = product_names.index(i)
correlation_product_ID = correlation_matrix[product_ID]
Recommend = list(X.index[correlation_product_ID > 0.80])

# Removes the item already bought by the customer
Recommend.remove(i) 

if selected_recommender == 'Type 1 (Rating Prediction)':
    
    results = get_predictions(user_id, recommender_result)
    for i in range(10):
        x = 2*i
        y = i + 1
        show_this = results[x][2:12]
        show_this1 = results[y][2:12]
        cols = st.beta_columns(2)
        cols[0].write(show_this)
        cols[1].write(show_this1)
else:
    for i in range(5):
        x = 2*i
        y = i + 1
        show_this = Recommend[x]
        show_this1 = Recommend[y]
        cols = st.beta_columns(2)
        cols[0].write(show_this)
        cols[1].write(show_this1)