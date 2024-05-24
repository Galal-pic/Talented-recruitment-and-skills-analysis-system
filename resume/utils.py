import spacy 
import PyPDF2
from spacy.tokens import DocBin
from tqdm import tqdm
import json
import numpy as np
import pandas as pd
from sentence_transformers.util import cos_sim
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

def extract_skills_from_pdf(pdf_path : str) -> str: 
    with open(pdf_path , 'rb') as pdf : 
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []
        for page in reader.pages:
            content=page.extract_text()
            pdf_text.append(content)
        pdf_text = "\n".join(pdf_text)
    nlp = spacy.load(r"Models\spacy_cv\model-last")
    doc = nlp(pdf_text)
    s = doc.ents
    return s


def sentence_embedding4_similarity_score_test(skills):
    l=[]
    for x in skills:
        l.append(str(x))
    new_skills = ', '.join(l)
    df = pd.read_csv('cvs/new_embedded_data.csv')

    model4 = SentenceTransformer('thenlper/gte-base')

    # Embedding the new skills
    skills_embeddings = model4.encode(new_skills).reshape(1, -1)

    # Convert string representations to NumPy arrays
    df['skills_embeddings'] = df['skills_embeddings'].apply(lambda x: np.fromstring(x[1:-1], dtype=np.float32, sep=' '))

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(np.vstack(df['skills_embeddings']), skills_embeddings)    
    

    top_indices = np.argsort(similarity_scores, axis=0)[-5:][::-1].flatten()

    # Collect top 5 most similar job titles and their similarity scores in a list
    top_job_titles = []
    for index in top_indices:
        job_title = df['Job Title'][index]
        similarity_score = similarity_scores[index][0]  # Extract similarity score from 2D array
        top_job_titles.append((job_title, similarity_score))

    job_title, similarity = top_job_titles[0]


    #replace with the highest similarity (title normalization)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    tech_df = pd.read_csv(r"Models\techh.csv")
    target_term = job_title
    job_titles = tech_df["job titles"]
    target_embedding = model.encode([target_term])
    job_title_embeddings = model.encode(job_titles)
    similarities = cosine_similarity(target_embedding, job_title_embeddings)[0]
    max_index = similarities.argmax()

    job_title = job_titles[max_index]

    return job_title, similarity 