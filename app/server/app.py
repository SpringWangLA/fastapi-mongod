from fastapi import FastAPI

from server.routes.student import router as StudentRouter

from server.routes.functiontest import router as FunctionTestRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(FunctionTestRouter, tags=["FunctionTest"], prefix="/functiontest")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
    