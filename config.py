import os


class Settings:
    """Application configuration loaded from environment variables."""

    # DATABASE_URL format examples:
    #   SQLite (dev fallback):  sqlite:///./household_power.db
    #   Azure SQL via pyodbc:   mssql+pyodbc://<user>:<pwd>@<server>.database.windows.net:1433/<db>?driver=ODBC+Driver+18+for+SQL+Server
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./household_power.db",
    )

    # App metadata
    APP_NAME: str = "Data Ingestion Service"
    APP_VERSION: str = "0.1.0"


settings = Settings()
