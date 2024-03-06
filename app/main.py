import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from db.config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)


@app.get("/")
async def Home():
    return HTMLResponse(
        """
<html>
  <head>
    <title>Travelix API</title>
    <link
      href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
      rel="stylesheet"
    />
    <style>
        @keyframes blink {
            0%, 100% { text-shadow: 0 0 0.5rem #3b; }
            50% { text-shadow: 0 0 0.8rem #38b; }
        }
        .blink:hover{
            animation: blink 2s infinite;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
            40% {transform: translateY(-30px);}
            60% {transform: translateY(-15px);}
        }
        .bounce {
            animation: bounce 2s;
        }
    </style>
  </head>
  <body style="background: #14141f" class="flex flex-col gap-16 my-16 mx-16">
    <a href="http://127.0.0.1:8000/redoc" class="flex text-blue-500 text-3xl font-medium blink bounce">Welcome to Travelix API</a>
    <div class="flex flex-col gap-8">
      <p class="text-gray-200 text-lg">
        Click
        <a
          class="font-medium text-blue-500 hover:text-blue-800"
          href="http://127.0.0.1:8000/redoc"
          >here</a
        >
        to view the project documentation.
      </p>
      <p class="text-gray-300 text-lg">
        FastApi is a modern, fast (high-performance), web framework for building
        APIs with Python 3.7+ based on standard Python type hints. It is
        designed to be easy to use and understand, and it is also highly
        performant. FastAPI is built on top of Starlette for the web parts and
        Pydantic for the data parts.
      </p>
      <div
        class="flex flex-col md:flex-row items-center gap-8 w-full font-medium"
      >
        <a
          href="http://127.0.0.1:8000/redoc"
          class="flex flex-row w-full md:w-96 bg-blue-500 hover:bg-blue-800 text-white p-4 rounded gap-2 justify-center items-center"
        >
          <p>View the project documentation</p>
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M9 5H7C6.46957 5 5.96086 5.21071 5.58579 5.58579C5.21071 5.96086 5 6.46957 5 7V19C5 19.5304 5.21071 20.0391 5.58579 20.4142C5.96086 20.7893 6.46957 21 7 21H17C17.5304 21 18.0391 20.7893 18.4142 20.4142C18.7893 20.0391 19 19.5304 19 19V7C19 6.46957 18.7893 5.96086 18.4142 5.58579C18.0391 5.21071 17.5304 5 17 5H15M9 5C9 4.46957 9.21071 3.96086 9.58579 3.58579C9.96086 3.21071 10.4696 3 11 3H13C13.5304 3 14.0391 3.21071 14.4142 3.58579C14.7893 3.96086 15 4.46957 15 5M9 5C9 5.53043 9.21071 6.03914 9.58579 6.41421C9.96086 6.78929 10.4696 7 11 7H13C13.5304 7 14.0391 6.78929 14.4142 6.41421C14.7893 6.03914 15 5.53043 15 5"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </a>
        <a
          href="https://fastapi.tiangolo.com/es/"
          class="flex flex-row w-full md:w-96 text-gray-50 border border-blue-500 hover:text-blue-500 hover:border-blue-800 p-4 rounded gap-2 justify-center items-center"
        >
          <p>Go to FastApi documentation</p>
          <svg
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M9 3H3C2.46957 3 1.96086 3.21071 1.58579 3.58579C1.21071 3.96086 1 4.46957 1 5V15C1 15.5304 1.21071 16.0391 1.58579 16.4142C1.96086 16.7893 2.46957 17 3 17H13C13.5304 17 14.0391 16.7893 14.4142 16.4142C14.7893 16.0391 15 15.5304 15 15V9M8 10L17 1M17 1H12M17 1V6"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </a>
      </div>
    </div>
  </body>
</html>
        """
    )
