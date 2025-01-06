import pandas as pd

from FlagEmbedding import FlagLLMReranker
from openai import OpenAI

from dotenv import load_dotenv
import os
import sys

import logging


logging.getLogger("transformers").setLevel(logging.ERROR)
os.environ["TOKENIZERS_PARALLELISM"] = "false"


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
reranker = FlagLLMReranker('BAAI/bge-reranker-v2-gemma', use_fp16=True)

def classify_news(news_df):
    news_df["Collaboration/Partnership"] = reranker.compute_score(
        [["Collaboration/Partnership", row["Headline"]] for _, row in news_df.iterrows()],
        normalize=True,
    )
    news_df["Industry Growth/Trends"] = reranker.compute_score(
        [["Industry Growth/Trends", row["Headline"]] for _, row in news_df.iterrows()],
        normalize=True,
    )
    news_df["Leadership Change"] = reranker.compute_score(
        [["Leadership Change", row["Headline"]] for _, row in news_df.iterrows()],
        normalize=True,
    )
    
    return news_df


def get_relevant_articles(user_goal, news_df):
    prompt = f"""
    The user has described their goal as: {user_goal}.
    
    Below are some news articles:
    {news_df["Headline"]}

    Please provide two articles that would help the user with their goal and explain why each article is relevant.
    Structure your answer exactly like this:
    1. [Write Headline here]
    [Write Reason here, around 30 words]
    """

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )
    content = completion.choices[0].message.content

    results = []
    rows = content.split("\n\n") 
    for row in rows:
        lines = row.split("\n")  
        result = {}
        if len(lines) >= 2: 
            result["Headline"] = lines[0][3:].strip('" ') 
            result["Reason"] = lines[1].strip()
            results.append(result)

    return pd.DataFrame(results)