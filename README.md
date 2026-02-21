### End To End Project Blog Generation Agentic AI 

# project is created using uv venv
# Install uv using 
pip install uv
# Create vertual environment using uv
uv init
uv venv
.venv\Scripts\activate

# Install anything using uv 
uv add -package_name

# To run the project using fastapi
python app.py

# To check in postman
request = POST
running on : http://127.0.0.1:8000/blogs
And Body/raw
{
    "topic":"Agentic AI" # Or anything as required
}
# To run and debug in the langgraph development studio 
langgraph dev

## Ensure
ensure both python app.py and langgraph dev are running at the same time

#Langgraph dependencies
{
    "dependencies":["."], # it refers to the current directory
    "graphs":{
        "blog_generator_agent":"./src/graphs/graph_builder.py:graph"  # Platform name with path and graph form graph_builder.py
    },
    "env":"./.env"
}