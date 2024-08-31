# -*- coding: utf-8 -*-
"""Task02.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SqH0EDceQm-ekjGIHniXkhFA59SKikzC
"""

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

# Load the dataset
df = pd.read_excel('/content/Online Retail.xlsx')

print(df.head())

# Data Preprocessing
df.dropna(subset=['CustomerID'], inplace=True)
df['CustomerID'] = df['CustomerID'].astype(int)

# Creating the user-item matrix
user_item_matrix = df.pivot_table(
    index='CustomerID',
    columns='StockCode',
    values='Quantity',
    aggfunc='sum',
    fill_value=0
)

# Converting the matrix to a sparse format
user_item_sparse = csr_matrix(user_item_matrix)

# Building the recommendation model using Nearest Neighbors
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(user_item_sparse)

# Function to recommend products
def recommend_products(customer_id, n_recommendations=5):
    customer_idx = user_item_matrix.index.get_loc(customer_id)
    distances, indices = model.kneighbors(
        user_item_sparse[customer_idx],
        n_neighbors=n_recommendations + 1
    )
    product_indices = indices.flatten()[1:]
    return user_item_matrix.columns[product_indices]

# Example usage
customer_id = user_item_matrix.index[0]
recommended_products = recommend_products(customer_id, n_recommendations=5)
print(f"Recommended products for customer {customer_id}:\n", recommended_products)