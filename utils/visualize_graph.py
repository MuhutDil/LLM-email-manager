# Create picture to graph
from graphs.notice_extraction import NOTICE_EXTRACTION_GRAPH
from graphs.email_agent import email_agent_graph

image_data = NOTICE_EXTRACTION_GRAPH.get_graph().draw_mermaid_png()
with open("notice_extraction_graph.png", mode="wb") as f:
    f.write(image_data)

image_data = email_agent_graph.get_graph().draw_mermaid_png()
with open("main_graph.png", mode="wb") as f:
    f.write(image_data)

