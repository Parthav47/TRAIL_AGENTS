#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
from article_agent.crew import ArticleAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        "theme": "India vs South Africa recent T20 Series",
    }
    
    try:
        result = ArticleAgent().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
if __name__=="__main__":
    run()