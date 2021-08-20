import pandas as pd
import numpy as np



df = pd.read_json('data/data.json')
print(df.head(2))


# Creating a dataframe with 50%
# values of original dataframe
part_50 = df.sample(frac = 0.5)
  
# Creating dataframe with 
# rest of the 50% values
rest_part_50 = df.drop(part_50.index)
  