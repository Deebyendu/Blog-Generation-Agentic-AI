from src.states.blogstate import BlogState
from langchain_core.messages import HumanMessage
from src.states.blogstate import Blog
class BlogNode:
    """
    A class to represent the blog node
    """
    def __init__(self,llm):
        self.llm = llm
    
    def title_creation(self,state:BlogState):
        """
        Create the title for the blog
        """
        if "topic" in state and state["topic"]: # it checks if "topic" in state i.e BlogState and state["topic"] checks is it empty string or not.
            prompt="""
            You are an expert blog content writer. Use Markdown formatting. Generate a blog title
            for the {topic}. This title should be creative and SEO frendly.
            """
            system_message=prompt.format(topic=state["topic"])
            response=self.llm.invoke(system_message)
            return {"blog":{"title": response.content}} # in blog state we are returning the title of the blog

    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt="""you are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}."""
            system_message=system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}# from blog state we are taking title and returning both title and content. If "title": state['blog']['title'] not present then it will loose the title that has been already generated. 

    def translation(self,state:BlogState):
        """
        Translate the blog content to the specified language
        """
        translation_prompt="""
        Translate the following content info {current_language}.
        - Maintain the original tone, style and formatting.
        - Adapt cultural references and idioms to be appropriate for  {current_language}.
        
        ORIGINAL CONTENT:
        {blog_content}
        """
        blog_content=state['blog']['content']
        messages=[
            HumanMessage(translation_prompt.format(current_language=state["current_language"], blog_content = blog_content))
        ]
        translation_content=self.llm.invoke(messages)
        return {"blog": {"content": translation_content}}
    
    def route(self,state:BlogState):
        return {"current_language":state['current_language']}     
    
    def route_decision(self,state:BlogState):
        """
        Decide the next blog state based on the current blog state.
        """
        if state["current_language"]=="hindi":
            return "hindi"
        elif state["current_language"]=="french":
            return "french"
        elif state["current_language"]=="spanish":
            return "spanish"
        else:
            return state["current_language"]