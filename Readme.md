# News Classification Demo

This repository demonstrates using the BAAI/bge-reranker-v2-gemma and OpenAI ChatGPT API to build a classification application.

## Prerequisites
- **Python**: Version 3.12.8
 
## Setup
- Install Requirements
  ```bash
  pip install -r requirements.txt
  ```
- Setup a env file for the openai API key (OPENAI_API_KEY)

## Run
```bash
python Terminal.py
```

## Agent Architecture and Decision-Making Process

### Overview

The **News Classification and Recommendation Agent** utilizes two key models to classify and rank news articles based on predefined themes and user-specific goals. These models are integrated into the system's workflow to make informed decisions about the relevance of articles to the user’s needs.

### Models Used

#### 1. **FlagLLMReranker (BAAI/bge-reranker-v2-gemma)**

- **Purpose:**  
  This model is used to rank news articles based on their relevance to predefined categories such as:
  - **Collaboration/Partnership**
  - **Industry Growth/Trends**
  - **Leadership Change**
- **When/Where Used:**
  - The **FlagLLMReranker** is called in the `classify_news()` function, where it scores each article's headline for each of the predefined categories. The model computes a relevance score for each article by comparing its headline to the category labels, which helps in assessing how closely the content of the article aligns with the themes of interest.
- **Why Used:**
  - The **FlagLLMReranker** is particularly suited for this task due to its ability to re-rank and assess the relevance of articles based on semantic understanding, improving the accuracy of classification tasks when working with a diverse set of articles.

#### 2. **OpenAI GPT-4o-mini**

- **Purpose:**  
  This language model is used to process user input and retrieve relevant articles based on the user's described goal. It can generate meaningful responses and rank articles based on their content in relation to the user’s goal.
- **When/Where Used:**

  - The **OpenAI GPT-4o-mini** model is invoked within the `get_relevant_articles()` function. When the user provides a goal (e.g., "Sell Cloud Services"), the system constructs a prompt that includes the goal and a list of article headlines. The model is tasked with selecting and explaining why certain articles are most relevant to the user’s specific goal.
  - The model then generates a response that includes two articles deemed most relevant to the goal, along with an explanation for why each article was chosen. This allows the agent to provide personalized article recommendations based on the user's objectives.

- **Why Used:**
  - **OpenAI GPT-4o-mini** excels in understanding complex natural language and can provide nuanced recommendations based on a user's stated goal. By using GPT, the agent ensures that the recommendations are not just based on keyword matching, but on a deeper understanding of the user's intent and how the articles align with that intent.

--

## News Classification Demo Instructions

1. **Start the Demo**:
   The demo begins by printing a welcoming message on the screen. You will be prompted to enter search terms.

2. **Fetch News Articles**:
   After entering the search terms, the demo will fetch news articles related to the provided keywords. The program will fetch up to 20 articles using the search terms provided.

3. **Specify Your Goal (Optional)**:
   You will be asked whether you have a specific goal in mind.

- If you choose `yes`, you will be asked to describe your goal (e.g., "Sell Cloud Services").

4. **Fetch Relevant Articles (If a Goal is Provided)**:
   If you specified a goal, the program will fetch articles that are most relevant to that goal. The program will search through the fetched articles to find the ones that best match your goal.
   **Output:** It will display two articles that could be relevant to your goal.

5. **Classify News Articles (If No Goal is Provided)**:
   If you do not have a specific goal, the demo will classify the articles based on predefined categories such as:

- Collaboration/Partnership
- Industry Growth/Trends
- Leadership Change

   The program uses a language model to classify the headlines of the fetched news articles.
  
   **Output:** The articles will be classified, and the program will then proceed to allow you to sort them based on the categories.

6. **Sort the Articles**:
   After the classification step, you will be prompted to choose how to sort the articles. The available options are:

- **Sort by Collaboration/Partnership**
- **Sort by Industry Growth/Trends**
- **Sort by Leadership Change**
- **Exit the demo**

   **Output:** The top articles for the selected category will be displayed.

7. **Repeat or Exit**:

   After sorting and displaying the results, the program will prompt you again to choose a sort option or exit.

---

## Example Workflow:

### Goal Specified

1. **Enter search terms:**

- Enter search terms, separated by commas: Criteo

2. **Specify your goal:**

- Do you have a specific goal in mind? (yes/no): yes
- Please describe your goal or what you are looking for: Sell Cloud Services

3. **Fetching relevant articles:**

- The demo will fetch and display two relevant articles that match your goal.

### Goal Unespecified

1. **Enter search terms:**

- Enter search terms, separated by commas: Criteo

2. **Specify your goal:**

- Do you have a specific goal in mind? (yes/no): no

4. **Classify articles (if no goal provided):**

- If you chose not to have a goal, the demo will classify the articles into the categories: Collaboration/Partnership, Industry Growth/Trends, or Leadership Change.

5. **Sort articles:**

- The demo will prompt you to choose a category to sort the articles by (e.g., `1` for Collaboration/Partnership).

6. **Display sorted articles:**

- The top articles sorted by your chosen category will be displayed.

7. **Repeat or exit:**

- You can continue sorting articles or exit the demo by selecting `4`.
