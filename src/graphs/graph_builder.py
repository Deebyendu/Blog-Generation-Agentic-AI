from langgraph.graph import StateGraph,START,END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.node.blog_node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm
        self.graph=StateGraph(BlogState)
    
    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic
        """
        self.blog_node_obj=BlogNode(self.llm)
        # Nodes
        self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)

        # Edges
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge( "content_generation", END)
        
        return self.graph

    def building_language_graph(self):
        """
        Build a graph for blog generations with inputs topic and language
        """
        #Nodes
        self.blog_node_obj=BlogNode(self.llm)
        # Nodes
        self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)
        self.graph.add_node("hindi_translation",lambda state: self.blog_node_obj.translation({**state, "current_language":"hindi"})) # **state means it will be overwritten by current_language key value pair. 
        self.graph.add_node("french_translation",lambda state: self.blog_node_obj.translation({**state, "current_language":"french"}))
        self.graph.add_node("spanish_translation",lambda state: self.blog_node_obj.translation({**state, "current_language":"spanish"}))
        self.graph.add_node("route",self.blog_node_obj.route)

        # Edges and Conditional edges
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge( "content_generation","route")
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "hindi": "hindi_translation",
                "french": "french_translation",
                "spanish": "spanish_translation"
            }
        )
        self.graph.add_edge( "hindi_translation", END)
        self.graph.add_edge( "french_translation", END)
        self.graph.add_edge( "spanish_translation", END)
        return self.graph

    def setup_graph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()
        elif usecase == "language":
            self.building_language_graph()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")

        return self.graph.compile()


## Below code is for the langsmith langgraph studio
llm=GroqLLM().get_llm()

# get the graph
graph_builder=GraphBuilder(llm)
graph=graph_builder.building_language_graph().compile()


