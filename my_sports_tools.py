from crewai.tools import tool

@tool("check_resource")
def check_resource(resource_name: str):
    """
    Checks if a sports database or API is available.
    Input should be the name of the resource (e.g., 'MatchStats_DB').
    """
    available_resources = ["MatchStats_DB", "PlayerBio_API", "LiveScore_API"]
    if resource_name in available_resources:
        return f"Resource {resource_name} is ONLINE."
    return f"Resource {resource_name} is OFFLINE."