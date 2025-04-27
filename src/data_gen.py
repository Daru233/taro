import pandas as pd
import numpy as np

def create_mock_dataframe():
    data = {
        'Time': np.linspace(0, 10, 50),
        'Value A': np.sin(np.linspace(0, 10, 50)) + np.random.randn(50) * 0.1,
    }
    df = pd.DataFrame(data)
    return df
