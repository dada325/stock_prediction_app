import os

# API Endpoints
GPT4_API_ENDPOINT = os.environ.get("GPT4_API_ENDPOINT", "DEFAULT_GPT4_ENDPOINT")
ALPHA_VANTAGE_API_ENDPOINT = os.environ.get("ALPHA_VANTAGE_API_ENDPOINT", "DEFAULT_ALPHA_VANTAGE_ENDPOINT")

# API Keys
GPT4_API_KEY = os.environ.get("GPT4_API_KEY", "DEFAULT_GPT4_KEY")
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "DEFAULT_ALPHA_VANTAGE_KEY")

# Model and Data Directories
MODEL_DIRECTORY = os.environ.get("MODEL_DIRECTORY", "models/")
DATA_DIRECTORY = os.environ.get("DATA_DIRECTORY", "data/")

# Other Configuration Parameters
LOOKBACK_WINDOW = int(os.environ.get("LOOKBACK_WINDOW", 60))
MAX_NUM_WORDS = int(os.environ.get("MAX_NUM_WORDS", 10000))
MAX_SEQUENCE_LENGTH = int(os.environ.get("MAX_SEQUENCE_LENGTH", 250))
