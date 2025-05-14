from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import faiss

def few_shot_examples(theme):


    path = r"/Themes Dataset/lightroom_theme_configs.csv"
    df = pd.read_csv(path)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    index = faiss.read_index("/full_index_faiss.index")
    query = model.encode([theme])

    distances, indices = index.search(query, k=2)
    top_indices = indices[0]  
    few_shot_themes = df["theme"].iloc[top_indices].tolist()
    few_shot_configs = df["config"].iloc[top_indices].tolist()

    return few_shot_themes, few_shot_configs
