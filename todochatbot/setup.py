from setuptools import setup, find_packages

setup(
    name="todochatbot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "python-dotenv==1.0.0",
        "PyJWT==2.8.0",
        "cohere==5.20.2",
        "sqlmodel==0.0.16",
        "sqlalchemy==2.0.23",
        "python-multipart==0.0.6",
    ],
    python_requires=">=3.7",
)