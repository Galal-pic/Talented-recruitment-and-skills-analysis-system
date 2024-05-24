import spacy 
import PyPDF2
from resume.huggingface import spacy_model,embedding_model
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import tensorflow as tf
df_jobs = pd.read_csv(r'cvs\data_with_vector_technology.csv')

def extract_skills_from_pdf(pdf_path : str) -> str: 
    with open(pdf_path , 'rb') as pdf : 
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = [page.extract_text() for page in reader.pages]        
    pdf_text = "\n".join(pdf_text)
    doc = spacy_model(pdf_text)
    skills = list(set([ent.text.title() for ent in doc.ents]))
    return skills

def sentence_embedding4_similarity_score_test(skills):
    df = pd.read_csv(r'cvs\data_with_vector_technology.csv')
    # Embedding the new skills
    skills_emb = embedding_model.embed_query(str(skills))
    skills_embeddings = tf.constant([skills_emb])

    df['new_skills_embeddings'] = df['vector'].apply(lambda x: np.fromstring(x[1:-1], dtype=np.float32, sep=', '))
    cosine_loss = tf.keras.losses.CosineSimilarity(axis=-1)

    df['similarity_score'] = df['new_skills_embeddings'].apply(lambda job_skill_tensor: (cosine_loss(job_skill_tensor, skills_embeddings).numpy() * -1))

    top_matches = df.nlargest(3, 'similarity_score')
    output = [(row['job_title'], row['similarity_score']) for _, row in top_matches.iterrows()]
    
    return output , skills_emb


def append_cv(cv_name, embedding,job_title,skills):
    existing_data = pd.read_csv('cvs\cv_embedding.csv')  # Corrected the backslash to forward slash for file path
    new_data = pd.DataFrame({'cv_name': [cv_name], 'embedding': [embedding],'job_title':[job_title]
                             ,'skills':[skills]})  # Ensure cv_name and embedding are lists
    appended_data = pd.concat([existing_data, new_data], ignore_index=True)
    appended_data.to_csv('cvs/cv_embedding.csv', index=False)


def append_cvs(cv_name,path,name):
    skills_list = extract_skills_from_pdf(path)
    jobs , embedding = sentence_embedding4_similarity_score_test(skills=skills_list)
    if name=='pdf':
        append_cv(cv_name,embedding,jobs,skills_list)
    return jobs,skills_list,embedding


def retrive_skills_from_data_fortitle(jobs):
    lis = []
    for title in jobs:
        skills = df_jobs[df_jobs['Job Title']==title[0]]['skills'].to_list()[0]
        technology = df_jobs[df_jobs['Job Title']==title[0]]['technology_skills'].to_list()[0]
        technical = df_jobs[df_jobs['Job Title']==title[0]]['technical_skills'].to_list()[0]
        lis.append((skills,technology,technical))
    return lis