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

    def get_apriori_recommendation(self, products, top_k=5):
        recommendation_list = []

        for product in products:
            if product in self.apriori_recommendations:
                recommendation_list += self.apriori_recommendations[product]
            
        recommendation_list = sorted(recommendation_list, key=lambda x: x['confidence'], reverse=True)

        recommendations = []
        recommendations_per_category = {}

        for recommendation in recommendation_list:
            if recommendation in recommendations:
                continue

            product_category = recommendation['product_category']
            if product_category not in recommendations_per_category:
                recommendations_per_category[product_category] = 0

            if recommendations_per_category[product_category] >=2:
                    continue
            
            recommendations_per_category[product_category] += 1

            recommendations.append(recommendation['product'])

            if len(recommendations) >= top_k:
                break

        return recommendations
    
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
    