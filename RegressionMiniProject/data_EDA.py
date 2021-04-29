import pandas as pd
import numpy as np

raw_data = pd.read_csv("./A_product_history.csv")
print(raw_data.head())
print(raw_data.info())