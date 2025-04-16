from dotenv import load_dotenv


def load_environment_variables(env_path):
    load_dotenv(env_path)
    print("Environment variables loaded.")
