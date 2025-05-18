from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import faiss
import os

model = SentenceTransformer("all-MiniLM-L6-v2")
index_path = os.path.join("full_index_faiss.index")
csv_path = os.path.join("Themes Dataset", "lightroom_theme_configs.csv")
index = faiss.read_index(index_path)
df = pd.read_csv(csv_path)

def few_shot_examples(theme, k=1):
    if not theme or not isinstance(theme, str):
        raise ValueError("Theme must be a non-empty string.")

    query = model.encode([theme])
    distances, indices = index.search(query, k=k)
    top_indices = indices[0]

    few_shot_themes = df["theme"].iloc[top_indices].tolist()
    few_shot_configs = df["config"].iloc[top_indices].tolist()

    return few_shot_themes, few_shot_configs
