import os
import dotenv
from copy import deepcopy
from openai import OpenAI
from .utils import get_chatbot_respnse, get_embedding
from pinecone import Pinecone
import json
import pandas as pd

class RecommendationAgent():
    def __init__(self, aprioroi_recommendations_path, popular_recommendations_path):
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"), 
            base_url=os.getenv("RUNPOD_CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME")
        
        with open(aprioroi_recommendations_path, 'r') as file:
            self.apriori_recommendations = json.load(file)
        
        self.popular_recommendations = pd.read_csv(popular_recommendations_path)
        self.products = self.popular_recommendations['product'].tolist()
        self.product_category = self.popular_recommendations['product_category'].tolist()

    def get_popular_recommendations(self, product_category = None, top_k=5):
        recommendation_df = self.popular_recommendations

        if type(product_category) == str:
            product_category = [product_category]

        if product_category is not None:
            recommendation_df = self.popular_recommendations[self.popular_recommendations['product_category'].isin(product_category)]
        recommendation_df = recommendation_df.sort_values(by='number_of_transactions', ascending=False).head(top_k)        
        
        if recommendation_df.shape[0] == 0:
            return []
        
        recommendations = recommendation_df['product'].tolist()
        return recommendations
    