import autogen
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from scholarly import scholarly
import json
from dotenv import load_dotenv
import os

load_dotenv()  
# Load environment variables
load_dotenv()

# Configure OpenAI
config_list = [
    {
        'model': 'gpt-4',
        'api_key': os.getenv('OPENAI_API_KEY'),
    }
]

# Agent configurations
assistant_config = {
    "seed": 42,
    "temperature": 0.7,
    "config_list": config_list,
}

# Create agents with Docker disabled
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A user proxy that coordinates the PDF downloading task.",
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False
    },
    human_input_mode="NEVER"  # Disable human input to avoid EOF errors
)

research_assistant = autogen.AssistantAgent(
    name="research_assistant",
    system_message="""Research Assistant that finds relevant PDF links based on the topic.
    You search through academic sources and provide detailed information about found PDFs.""",
    llm_config=assistant_config,
)

download_manager = autogen.AssistantAgent(
    name="download_manager",
    system_message="""Download Manager that handles the downloading and saving of PDFs.
    You ensure proper file naming and organization.""",
    llm_config=assistant_config,
)

quality_control = autogen.AssistantAgent(
    name="quality_control",
    system_message="""Quality Control agent that verifies downloads and ensures content relevance.
    You check file integrity and content appropriateness.""",
    llm_config=assistant_config,
)

def download_pdf(url, filename):
    """Download a PDF file from the given URL."""
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            os.makedirs('downloads', exist_ok=True)
            filepath = os.path.join('downloads', filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded: {filename}")
            return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
    return False

def initiate_task(topic, num_papers=3):
    """Initiate the PDF downloading task with the given topic."""
    
    # Create a chat group for the agents
    groupchat = autogen.GroupChat(
        agents=[user_proxy, research_assistant, download_manager, quality_control],
        messages=[],
        max_round=50
    )
    
    manager = autogen.GroupChatManager(groupchat=groupchat)

    # Start the task
    user_proxy.initiate_chat(
        manager,
        message=f"""
        Please help me download {num_papers} PDF papers about "{topic}". 
        Follow these steps:
        1. Research Assistant: Search for relevant papers and provide their details
        2. Download Manager: Download the PDFs and save them properly
        3. Quality Control: Verify the downloads and check content relevance
        
        Let's maintain a structured approach and ensure we get high-quality papers.
        """
    )

class ResearchTools:
    @staticmethod
    def search_papers(query, num_results=3):
        """Search for academic papers using Google Scholar."""
        search_query = scholarly.search_pubs(query)
        results = []
        try:
            for i in range(num_results):
                paper = next(search_query)
                results.append({
                    'title': paper.bib.get('title'),
                    'author': paper.bib.get('author'),
                    'url': paper.bib.get('url'),
                    'year': paper.bib.get('year')
                })
        except StopIteration:
            pass
        return results

if __name__ == "__main__":
    # Create downloads directory if it doesn't exist
    os.makedirs('downloads', exist_ok=True)
    
    # Example usage
    topic = "machine learning optimization algorithms"
    initiate_task(topic)