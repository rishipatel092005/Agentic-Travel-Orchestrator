
import logging
import time

from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

logger = logging.getLogger(__name__)
MAX_WORKFLOW_ITERATIONS = 3
WORKFLOW_RECURSION_LIMIT = 20


class GraphBuilder:
    def __init__(self,model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self,state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        started_at = time.perf_counter()
        response = self.llm_with_tools.invoke(input_question)
        logger.info("llm_seconds=%.3f", time.perf_counter() - started_at)
        return {"messages": [response]}
    def build_graph(self):
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        self.graph = graph_builder.compile()
        return self.graph
        
    def __call__(self):
        return self.build_graph()


_graph_cache: dict[str, object] = {}


def get_travel_graph(model_provider: str = "groq"):
    """Return one compiled graph per model provider for the process lifetime."""
    if model_provider not in _graph_cache:
        _graph_cache[model_provider] = GraphBuilder(model_provider=model_provider)()
        logger.info("Compiled travel graph for provider=%s", model_provider)
    return _graph_cache[model_provider]


def invoke_travel_graph(graph, question: str):
    """Invoke the graph with a hard limit of two tool/re-planning cycles."""
    started_at = time.perf_counter()
    result = graph.invoke(
        {"messages": [question]},
        config={"recursion_limit": WORKFLOW_RECURSION_LIMIT},
    )
    logger.info("workflow_seconds=%.3f", time.perf_counter() - started_at)
    return result