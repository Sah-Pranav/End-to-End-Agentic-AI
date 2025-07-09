from fastapi.responses import JSONResponse
from logger.logging import logger

def log_exception(context, exception):
    """Logs error details using central logger."""
    logger.error(f"Error in {context}: {str(exception)}")

def handle_tool_exception(context, exception):
    """Handles exceptions in tool classes."""
    log_exception(context, exception)
    return f"Error occurred in {context}: {str(exception)}"

def handle_fastapi_exception(context, exception):
    """Handles exceptions in FastAPI routes."""
    log_exception(context, exception)
    return JSONResponse(status_code=500, content={"error": f"{context} failed: {str(exception)}"})

def handle_general_exception(context, exception):
    """Handles general exceptions in backend or workflow code."""
    log_exception(context, exception)
    return f"An error occurred in {context}: {str(exception)}"
