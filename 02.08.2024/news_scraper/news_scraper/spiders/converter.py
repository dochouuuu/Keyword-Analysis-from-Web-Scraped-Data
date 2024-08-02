import pandas as pd

def add_indexing_column(input_csv, output_csv):
    # Import the CSV file
    df = pd.read_csv(input_csv)
    
    # Add an indexing column at the front
    df.insert(0, 'Index', range(1, len(df) + 1))
    
    # Export the result as a new CSV file
    df.to_csv(output_csv, index=False)

# Example usage
add_indexing_column('finalres_pt1_old.csv', 'output.csv')


