from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai import LLM
from crewai_tools import SerperDevTool
import os
from typing import List

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

mistral_llm = LLM(
    model="openrouter/mistralai/mistral-7b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7
)

search_tool = SerperDevTool()
@CrewBase
class ArticleAgent():
    """ArticleAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def content_strategist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist_agent'], 
            llm=gemini_llm,
            verbose=True
        )

    @agent
    def designer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['designer_agent'], 
            llm=gemini_llm,
            verbose=True
        )

    @agent
    def researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_agent'],
            llm=mistral_llm, 
            tools=[search_tool],
            verbose=True
        )

    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'], 
            llm=mistral_llm,
            verbose=True
        )

    @task
    def content_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_strategy_task'], 
            output_file="output/content_strategy.md",
            verbose=True
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'], 
            output_file="output/design.md",
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], 
            output_file="output/research.md",
            verbose=True
        )

    @task
    def write_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_task'],
            output_file="output/final_article.md",
            verbose=True
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )