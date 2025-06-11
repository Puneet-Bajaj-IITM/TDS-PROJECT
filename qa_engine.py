import json
import os
from typing import List, Optional, Tuple
from bs4 import BeautifulSoup
from openai import OpenAI
import dotenv
import base64
import jsonlines
import hashlib
from schemas import AskResponse, Link
from langchain_core.output_parsers import PydanticOutputParser

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATA_PATH = 'data/posts.json'
OPENAI_MODEL = "gpt-4.1-2025-04-14"

client = OpenAI(api_key=OPENAI_API_KEY)

# LangChain imports
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# Load posts
with open(DATA_PATH, 'r') as f:
    posts = json.load(f)

# Extract plain text from HTML (forum)
discourse_texts = []
discourse_metadatas = []
for i, post in enumerate(posts):
    soup = BeautifulSoup(post.get('text', ''), 'html.parser')
    text = ""
    for element in soup.stripped_strings:
        if element.startswith('http'):
            text += f" [URL: {element}] "
        else:
            text += element + " "
    discourse_texts.append(text.strip())
    discourse_metadatas.append({"url": post["url"]})


course_content_texts = []
course_content_metadatas = []
# --- Enrich with CourseContentData.jsonl ---
course_content_path = 'data/CourseContentData.jsonl'
if os.path.exists(course_content_path):
    with jsonlines.open(course_content_path) as reader:
        for obj in reader:
            content = obj.get('content', '')
            url = obj.get('url', '')
            if content:
                course_content_texts.append(content.strip())
                course_content_metadatas.append({"url": url, "source": "course_content"})

# --- Deduplicate before indexing ---
def hash_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

all_texts = discourse_texts + course_content_texts
all_metadatas = discourse_metadatas + course_content_metadatas
seen_hashes = set()
dedup_texts = []
dedup_metadatas = []
for text, meta in zip(all_texts, all_metadatas):
    h = hash_text(text)
    if h not in seen_hashes:
        seen_hashes.add(h)
        dedup_texts.append(text)
        dedup_metadatas.append(meta)

# Set up OpenAI embeddings and a single vector store
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")
vector_store = InMemoryVectorStore(embedding_model)
vector_store.add_texts(dedup_texts, metadatas=dedup_metadatas)

def get_image_description(image_b64: str) -> str:
    """Get a description of the image from GPT-4o."""
    prompt = "Describe the content of this image in detail for a teaching assistant helping with data science questions."
    messages = [
        {"role": "system", "content": "You are a helpful teaching assistant for the IIT Madras Data Science course."},
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
        ]}
    ]
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI error: {e}]"

def answer_question(question: str, image: Optional[str] = None) -> Tuple[str, List[dict]]:
    image_desc = None
    if image:
        # If image is a file path, convert to base64
        if os.path.isfile(image):
            with open(image, "rb") as img_file:
                image = base64.b64encode(img_file.read()).decode("utf-8")
        image_desc = get_image_description(image)
    # Use both question and image description for context search
    if image_desc:
        search_query = f"{question}\nImage description: {image_desc}"
    else:
        search_query = question
    # Search for top 10 similar contexts
    results = vector_store.similarity_search(search_query, k=10)
    context_texts = [f"Context {i+1}: {doc.page_content}" for i, doc in enumerate(results)]
    context = "\n\n".join(context_texts)
    # Compose the final prompt for GPT-4o (do NOT send the image, only its description)

    parser = PydanticOutputParser(pydantic_object=AskResponse)

    if image_desc:
        prompt = (
            f"You are a helpful teaching assistant for the IIT Madras Data Science course. "
            f"A student asked: '{question}'.\n"
            f"Image description: {image_desc}\n"
            f"Here are some relevant forum posts:\n{context}\n"
            f"Based on the question, the image description, and the forum posts, answer the student's question in a clear and concise way. Include any relevant links from the forum posts as the citations. Output shall always answer the question not just information. Dont make up answers if the information is not present in the context. remember to use the citations in the answer. Dont give answers conflicting to question statement. {parser.get_format_instructions()}"
        )
    else:
        prompt = (
            f"You are a helpful teaching assistant for the IIT Madras Data Science course. "
            f"A student asked: '{question}'.\n"
            f"Here are some relevant forum posts:\n{context}\n"
            f"Based on these, answer the student's question in a clear and concise way. Include any relevant links from the forum posts as the citations. output shall always answer the question not just information. Dont make up answers if the information is not present in the context. remember to use the citations in the answer. Dont give answers conflicting to question statement {parser.get_format_instructions()}"
        )
    messages = [
        {"role": "system", "content": "You are a helpful teaching assistant for the IIT Madras Data Science course."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=1024
        )
        answer_text = response.choices[0].message.content.strip()
        answer = parser.parse(answer_text)
    except Exception as e:
        answer_text = f"[OpenAI error: {e}]"
    links = []
    for doc in results:
        meta = doc.metadata
        answer.links.append(Link(url=meta['url'], text=doc.page_content))
    return answer

if __name__ == "__main__":
    def load_image(path: str) -> str:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    print(answer_question("Should I use gpt-4o-mini which AI proxy supports, or gpt3.5 turbo?", image=load_image("image.png")))