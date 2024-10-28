from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate/", response_class=HTMLResponse)
async def calculate(request: Request, num1: float = Form(...), num2: float = Form(...), operation: str = Form(...)):
    result = None
    error = None

    if operation == 'add':
        result = num1 + num2
    elif operation == 'sub':
        result = num1 - num2
    elif operation == 'mult':
        result = num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            error = "Cannot divide by zero"
    else:
        error = "Invalid operation"

    # Convert result to an integer if it has no decimal value
    if result is not None and result.is_integer():
        result = int(result)
    
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "error": error})

