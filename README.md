# Cognitia
![Logo](images/logo.png)


<details>
  <summary><strong>ℹ️ Information About Team and Product</strong></summary>
  &nbsp;

&emsp;&emsp; *Cognitia* is an AI-powered decision support tool designed for mental health professionals. It helps clinicians interpret psychological test results efficiently and consistently. By transforming raw test scores into structured insights using machine learning, Cognitia supports early identification of mental health risks, provides AI-generated summaries, enhances diagnostic clarity and fasten the diagnose process. The platform prioritizes data privacy, and alignment with clinical workflows, making it a reliable companion in psychological evaluation.

  ### 👥 Team Members

  | Name              | Title           | Communication |
  |-------------------|------------------|---------|
  | Damla Demirok     | Scrum Master   |  [LinkedIn](https://www.linkedin.com/in/damla-demirok-00a918284/)      |
  | Hamza Tulmaç      | Developer      | [LinkedIn](https://www.linkedin.com/in/hamza-tulmac-57548217b/)        |


</details>

---

<details>
  <summary><strong>📦 Product Description and Main Aim</strong></summary>
  &nbsp;
  
&emsp;&emsp;This project aims to develop a web-based mental health decision support system that integrates standardized psychological tests with machine learning models. Through a two-stage AI pipeline, the system will first analyze user-submitted test scores, then transform them to more academic baseline. After that it will generate evidence-based probability distribution on mental illness types to support clinicians in their decision-making process. The project follows an agile development methodology over three sprints, focusing on model training, interface design, and clearity. Ultimately, the goal is to deliver a functional prototype tailored for psychiatrists and psychologists, offering a lightweight yet scientifically grounded evaluation tool.


</details>

---

<details>
  <summary><strong>🔍 Product Features</strong></summary>

  - Standardized Test Input
Clinicians will recieve extracted results from an algorithm. 

- Machine Learning-Based Evaluation
Those test responses are processed by a trained ML model to classify mental health risk levels with consistency and accuracy.

- AI-Generated Interpretation
An LLM or rule-based system provides brief, understandable, and clinically relevant summaries of the test outcome.

- Risk Level Visualization
Results are displayed with visual indicators (e.g., low / moderate / high risk), enabling quick comprehension.

- Data Privacy & Security
The system ensures that all patient inputs remain anonymous and are processed in accordance with ethical standards.

- Web-Based Interface
Doctors can access the system via a clean, user-friendly interface—no installation required.

- Modular & Extendable
The product is built to support new tests, models, and languages, allowing for future clinical use cases.

</details>

---

<details>
  <summary><strong>🎯 Target Audience</strong></summary>
 &nbsp;
  
- Psychiatrists
- Clinical psychologists
- General practitioners
- Mental health professionals working in clinical settings


</details>

---

### 🚀 Sprint 1

#### 📝 Notes:
- Team name, member roles, and project name were finalized.  
- GitHub repository was created with a structured folder setup.  
- Product mission, vision, and core values were written.  
- The color palette and font selection process started; a draft version was decided.
- First front-end of the site built.
- Figma-based logos were prepared.  
- A user flow diagram (from test input to result report) was created on draw.io.  
- Initial logo concept was developed.      
- Sprint 1 report was written and finalized.  

#### 🎯 Total Points / How We Decide:
- **Target:** 90 points  
- **Completed:** 90 points  
- Points are distributed based on task complexity and estimated effort.  
- Sprint 1 target is lower due to the initialization part of the project.

#### 🔄 Daily Scrum:
- Conducted daily with the messages and weekly voice calls. 

 
- 🚧 **In Progress:**
  - Website development  
  - Data cleaning  
- ⏭️ **Upcoming:**
  - Model architecture setup  
  - Form structure & JSON transformation  
  - Answer-to-score algorithm

#### 🔍 Review:
- The team compleated point expectations.  
- Strong collaboration was observed during UI and flow planning.  
- Decision processes for design (color/logo) took more time than expected.  
- Clear direction was set for Sprint 2 deliverables.

<details>
  <summary>📸 Screenshots & Files</summary>

- [Project Charter (PDF)](images/sprint1/YZA%20-%20Bootcamp_Project%20Charter.pdf)
- [User Flow (drawio)](images/sprint1/cognitia_flow.drawio.pdf)
- [Project Plan (PNG)](images/sprint1/sprint1_projectplan.png)

</details>

</details>

---

### 🚀 Sprint 2

#### 📝 Notes:
- [Landing Page](images/sprint2/websiteproto) has been starting to initialize.  
- Classification data selected from [Harvard's public dataset](https://dataverse.harvard.edu/file.xhtml?fileId=7440350&version=1.1)
- Data analysis and encoding is done using [Google Colab](https://colab.research.google.com/drive/1BTZX11qrY4josVxjID8QFkFvOXPcXtzf?usp=sharing)
- Questions are decided respect to other clinical questionnaires(in terms of questions, length etc.)


#### 🎯 Total Points:
- **Target:**  140 Points
- **Completed:**  150 Points
- Sprint 2 ended early so as extra we prepared the [Ethical Statement](https://docs.google.com/document/d/1Bh-4gYXUC1pPVznx-Ngl7EjBePhMJgEgUgTbrUgjbGw/edit?usp=sharing)

#### 🔄 Daily Scrum:
- Conducted daily with the messages and weekly voice calls.
- Plus we connected in our sheets' comment sections.

 
- 🚧 **In Progress:**
  - Basic XGBoost model setup (classification logic)
  - Data cleaning script finalization
- ⏭️ **Upcoming:**
  - Evaluation of test results using XGBoost predictions
  - Integration of backend with form logic
  - Finalization of frontend interface
  - Uploading **cleaned** dataset and code to GitHub
  - Preparing user test scenario & presentation video
  - Feature importance visualization for model

#### 🔍 Retrospective:
-  **What went well?**
  -  The team successfully created and cleaned the dataset ahead of schedule.
  -  Question mapping logic was discussed clearly and applied effectively.
  -  Task ownership was well distributed and completed collaboratively.
  -  Psychological test design and form conversion worked seamlessly.
-  **What didn’t go well?**
  -  Due to communication problems, frontend preview delayed
-  **What can we improve?**
  -  Time estimation for the video and main ML was slightly underestimated.
  -  **What should we change next time?**
  -  For the meetings we can make our meetings more frequently
  -  
#### 🔍 Review:
- The team exceed point expectations.  
- We compleated the sprint early so worked on tiny tasks.
- Concluded that integration from ML to web will take time  
- We had some communication issues about test results' first evaluation proccess(solved).
<details>
  <summary>📸 Screenshots & Files</summary>
  
- [Project Plan and Points](images/sprint2/sprint2_projectplan.png)

</details>

</details>

---

### 🚀 Sprint 3

#### 📝 Notes:
- [Data](cognitia_dataset.csv) to train the model is finalized.
- For [Main Model](BootcampMain.ipynb) XGBoost used and trained.
- [Test Cases](images/sprint3/CognitiaTestCases.pdf) for professionals and cliends are created.
- Main model uploaded to the website.
- [Project Video](https://youtu.be/Pn_eKAuOYPM) is prepared.


#### 🎯 Total Points:
- **Target:**  120
- **Completed:**  105
- We faced challenges integrating the model and code into the website due to unexperiencedness.

#### 🔄 Daily Scrum:
- Conducted daily with the messages and voice calls.

 

#### 🔍 Retrospective:
-  **What went well?**
  - We successfully developed both the ML model and the website interface.
-  **What didn’t go well?**
  - Unexpected device problems caused a delay.
  - Connection between ML model and website lacked.
-  **What can we improve?**
  -  Start integration between frontend and backend earlier.
  -  Plan more buffer time for potential technical issues.
  -  Improve testing and deployment practices.



#### 🔍 Review:
- We designed a psychological decision-support ML model predicting diagnosis probabilities.
- Although we faced integration difficulties, the final model reflected the core functionality and design goals.
- The project helped us understand teamwork, agile planning, and the importance of early testing.

  
<details>
  <summary>📸 Screenshots & Files</summary>
  
- [Project Plan and Points](images/sprint3/sprint3_projectplan.png)

</details>

</details>

## 📎 License

This project is licensed under the [MIT License](LICENSE).

