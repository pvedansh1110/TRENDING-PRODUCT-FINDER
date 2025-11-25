
import pandas as pd

def load_data(path="shopping_trends.csv"):
    """Load main shopping dataset."""
    df = pd.read_csv(path)
    return df

def generate_trending_products(input_path="shopping_trends.csv", output_path="trending_products.csv"):
    """Generate trending products based on purchase frequency."""
    df = load_data(input_path)

    trending = (
        df.groupby(["Item Purchased", "Category"])
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    trending.to_csv(output_path, index=False)
    return trending


if __name__ == "__main__":
    print("Generating trending products file...")
    result = generate_trending_products()
    print("Trending products saved!")
    print(result.head())
