import os
from dotenv import load_dotenv


def set_env_from_dotenv(dotenv_path=".env"):
    """
    Set environment variables from a .env file.

    Args:
    - dotenv_path (str): Path to the .env file. Defaults to ".env".
    """
    # Load environment variables from .env file
    load_dotenv(dotenv_path)

    # Iterate through loaded environment variables and set them in os.environ
    for key, value in os.environ.items():
        os.environ[key] = value

    print(f"Environment variables set from {dotenv_path}")


if __name__ == "__main__":
    set_env_from_dotenv()
