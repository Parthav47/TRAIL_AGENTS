from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import TavilySearchTool, ScrapeWebsiteTool, DirectoryReadTool

from dotenv import load_dotenv
load_dotenv()

@CrewBase
class BlogCrew():

    agents_config="config/agent.yaml"
    tasks_config="config/task.yaml"

    @agent
    def researcher(self)->Agent:
        return Agent(
            config=self.agents_config['research_agent'],
            tools=[ TavilySearchTool(), ScrapeWebsiteTool() ],
            verbose =True
        )
    
    @agent
    def writer(self)->Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            tools=[ DirectoryReadTool() ],
            verbose =True
        )
    
    @task
    def research_task(self)->Task:
        return Task(
            config=self.tasks_config["researcher_task"],
            agent=self.researcher(),
            verbose=True
        )
    
    @task
    def blog_task(self)->Task:
        return Task(
            config=self.tasks_config["blog_task"],
            agent=self.writer(),
            verbose=True
        )
    @crew
    def crew(self)->Crew:
        return Crew(
            agents=[self.researcher(), self.writer()],
            tasks=[self.research_task(), self.blog_task()]
        )


if __name__ == "__main__":
    blog_crew=BlogCrew()
    result=blog_crew.crew().kickoff(inputs={"topic":"Impact of AI on Modern Education"})
    print(result)
    #print(blog_crew.tasks_config)