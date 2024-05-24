import spacy 
import PyPDF2
from resume.huggingface import spacy_model,embedding_model,normalize_jobtitle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
df_jobs = pd.read_csv(r'cvs\new_embedded_data.csv')

def extract_skills_from_pdf(pdf_path : str) -> str: 
    with open(pdf_path , 'rb') as pdf : 
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []
        
        for page in reader.pages:
            content=page.extract_text()
            pdf_text.append(content)
            
        pdf_text = "\n".join(pdf_text)
    doc = spacy_model(pdf_text)
    s = doc.ents
    l=[]
    for x in s:
        l.append(str(x))
    l = list(set([word.title() for word in l])) 
    return l

def sentence_embedding4_similarity_score_test(skills):
    df = pd.read_csv(r'cvs\new_embedded_data.csv')
    new_skills = ', '.join(skills)
    # Embedding the new skills
    skills_embeddings = embedding_model.encode(new_skills).reshape(1, -1)
    df['new_skills_embeddings'] = df['skills_embeddings'].apply(lambda x: np.fromstring(x[1:-1], dtype=np.float32, sep=' '))
    similarity_scores = cosine_similarity(np.vstack(df['new_skills_embeddings']), skills_embeddings)    
    top_indices = np.argsort(similarity_scores, axis=0)[-5:][::-1].flatten()
    top_job_titles = []
    for index in top_indices:
        job_title = df['Job Title'][index]
        similarity_score = similarity_scores[index][0]  # Extract similarity score from 2D array
        # top_job_titles.append((job_title, similarity_score))                              --> for the similarity score not percentage
        # Normalize similarity score to a percentage
        similarity_percentage = (similarity_score + 1) * 50  # Normalize to 0-100 scale    
        top_job_titles.append((job_title, similarity_percentage))
    output = [(first, round(second, 2)) for first, second in top_job_titles]
    # output = [(normalize_jobtitle(first), round(second, 2)) for first, second in top_job_titles]
    # df = pd.DataFrame(output, columns=['title', 'percentage'])
    # grouped_df = df.groupby('title')['percentage'].mean().reset_index().to_records(index=False)
    # grouped_df = sorted(grouped_df,key=lambda x : x[1],reverse=True)
    return output , skills_embeddings


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