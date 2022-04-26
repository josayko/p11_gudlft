from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "./env.development")
load_dotenv(dotenv_path=dotenv_path)
