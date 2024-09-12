from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load the dataset
df = pd.read_csv("pokemon.csv")
