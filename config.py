from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), "./env.development")
load_dotenv(dotenv_path=dotenv_path)
