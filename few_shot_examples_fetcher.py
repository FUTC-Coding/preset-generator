from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import faiss
import os

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(r"C:\Users\niket\OneDrive\Data Science\4. Semester\Cloud Computing and Distributed Systems\preset-generator\full_index_faiss.index")
df = pd.read_csv(r"C:\Users\niket\OneDrive\Data Science\4. Semester\Cloud Computing and Distributed Systems\preset-generator\Themes Dataset\lightroom_theme_configs.csv")

def few_shot_examples(theme, k=2):
    if not theme or not isinstance(theme, str):
        raise ValueError("Theme must be a non-empty string.")

    query = model.encode([theme])
    distances, indices = index.search(query, k=k)
    top_indices = indices[0]

    few_shot_themes = df["theme"].iloc[top_indices].tolist()
    few_shot_configs = df["config"].iloc[top_indices].tolist()

    return few_shot_themes, few_shot_configs
