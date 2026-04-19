'''
Purpose:

reads news headlines
returns sentiment (positive/neutral/negative)'''
from transformers import pipeline

sentiment = pipeline("text-classification", model="ProsusAI/finbert")