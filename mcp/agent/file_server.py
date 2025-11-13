from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("File Server")


# Load contents of the file 
@mcp.tool()
def load_file(filename : str) -> str:
    """Reads the contents of the given file"""
    with open(filename, "rt") as f:
        return f.read()


 
mcp.run(transport="stdio")
