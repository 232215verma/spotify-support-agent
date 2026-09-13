import pandas as pd

def create_labeling_sample(input_path="data/pairs_spotify.csv", n=200, seed=42):
    df = pd.read_csv(input_path)
    
    # Random sample for reading — seed fixed so it's reproducible
    sample = df.sample(n=n, random_state=seed).reset_index(drop=True)
    
    # Add empty columns for you to fill in while reading
    sample["intent"] = ""
    sample["notes"] = ""
    
    sample.to_csv("data/labeling_sample.csv", index=False)
    print(f"Saved {len(sample)} random examples to data/labeling_sample.csv")
    print("\nOpen this in Excel and read through customer_text column.")
    print("As you read, jot down repeating themes in a notes app —")
    print("we'll turn those into your final intent categories.")

if __name__ == "__main__":
    create_labeling_sample(n=200)