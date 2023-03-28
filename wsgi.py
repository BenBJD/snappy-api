import uvicorn

if __name__ == "__main__":
    uvicorn.run("snappy:app", reload=False, host="0.0.0.0")
