<a name="readme-top"></a>
<br />
<div align="center">
  <a href="https://github.com/Galal-pic/Talented-recruitment-and-skills-analysis-system">
    <img src="https://github.com/Galal-pic/Talented-recruitment-and-skills-analysis-system/blob/master/resume/static/images/logo_new.png" alt="Logo" width="120" height="120">
  </a>
  
  <h2 align="center">Talented-recruitment-and-skills-analysis-system</h2>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#Abstract"> Project Description</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#Dataset">Dataset</a></li>
    <li><a href="#Models">Models</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Project Description
We're revolutionizing the hiring landscape by integrating diverse language models (LM), deep learning techniques, and insightful analysis. At the core of our initiative are innovative bracelets designed to bridge the gap between job seekers and their ideal career prospects.

Our state-of-the-art system transforms the job search process by meticulously scanning and analyzing job descriptions from over four leading hiring platforms. We identify the essential skills required for various positions, laying the foundation for success in today's competitive job market.

Through advanced techniques in resume and job description analysis, our system seamlessly aligns extracted skills with those showcased on a job seeker's resume. This enables a comprehensive evaluation of the alignment between candidate skills and market demands. Additionally, we detect any skill gaps or deficiencies in a candidate's profile and provide personalized recommendations and advertisements for skill enhancement or training opportunities.

But we don't stop there. We're committed to simplifying the hiring process for businesses as well. By providing tailored resumes precisely aligned with their job descriptions, we enhance efficiency and effectiveness in their hiring endeavors.

### In this project, we address the needs of two key stakeholders: 
- **Job seeker**, who seeks roles aligned with their skills and desires insights into areas for skill enhancement to secure their dream job
- **Recruiter**, who aims to procure the most fitting CVs by defining job requirements and essential skills.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Usage
- If you are looking for a job, you can submit your CV, and we will show you which jobs are suitable for you and what skills are required for them. Through our analysis of over 15,000 job descriptions, we can share with you the skills most frequently needed for the job you want. We will also offer you job opportunities that you can register for directly.
  
  <div style="text-align: center;">
    <img src="https://github.com/Galal-pic/Talented-recruitment-and-skills-analysis-system/assets/70837846/18f45491-f203-4c59-90dc-5c548ae41a24" alt="uploadcv" style="width: 800px; height: auto; margin: 20px 0;">
  </div>

- If you are a recruiter looking for talented individuals, we can assist you by creating the job description for the position. We will analyze this description and extract the important skills. Then, we will find the best candidates for you and present their biographies.

  <div style="text-align: center;">
    <img src="https://github.com/Galal-pic/Talented-recruitment-and-skills-analysis-system/assets/70837846/58fc64e1-709c-4d5d-8194-a5175b604dd7" alt="Capture" style="width: 800px; height: auto; margin: 20px 0;">
  </div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Dataset
We collected data from various recruitment platforms like `Wuzzuf`, `Indeed`, `LinkedIn`, and `Glassdoor`, extracting details such as **job titles**, **descriptions**, and **company names**. Using the `Selenium` library, we automated the process of data extraction. Leveraging this data, we utilized large language models such as `GPT` to annotate job descriptions and identify essential skills. This process facilitated the effective preparation of data for further analysis and utilization in our project.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Models
We used the transformer library to train several models
1. I fine-tuned the `BERT` model for the task of extracting skills from job descriptions and achieved an accuracy rate of more than `91%`. This success underscores the effectiveness of the BERT model in accurately identifying and extracting relevant skills from textual data.

 Training Loss | Validation Loss | Precision | Recall | F1 | Accuracy |
---------------|-----------------|-----------|--------|----|----------|
 0.025200      | 0.041385        | 0.906973  | 0.916096 | 0.916434 | 0.987095 |

2. In our CV analysis process, we employed `spaCy` to fine-tune a small English model for training on CVs, to extract skills.
3. We employed `sentence transformation` in text representation to assist in calculating the percentage of similarity between each skill listed in the CV and the required skills for the specific job. This helped determine the degree of suitability for each candidate."
<p align="right">(<a href="#readme-top">back to top</a>)</p>





