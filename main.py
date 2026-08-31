from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel

class AdInput(BaseModel):
    ad_cost: int
    channel: str = "online"

app = FastAPI()
df = pd.read_csv('products.csv')
df['price'] = df['price'].astype(int)   # numpy.int64 → 파이썬 int

@app.get("/products")
def get_products():
    return df.to_dict(orient='records')


@app.get("/products/search")
def search_products(category: str | None = None, max_price: int | None = None):
    result = df

    if category is not None:
        result = result[result['category'] == category]
    if max_price is not None:
        result = result[result['price'] <= max_price]

    return {
        "count": len(result),
        "items": result.to_dict(orient='records')
    }