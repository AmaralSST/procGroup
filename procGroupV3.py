import pandas as pd

def get_equivalent_string(cell):
    cell = str(cell)  # Convert to string to ensure we don't get errors when splitting
    codes = cell.split(',')
    
    # Strip whitespaces and sort
    codes = sorted([code.strip() for code in codes])
    
    replaced_codes = []
    for code in codes:
        # If the code has an equivalent and the equivalent isn't the code itself
        # add it with "OR", else just append '-'
        if code in equivalents_map and code != equivalents_map[code]:
            replaced_codes.append(f"{equivalents_map[code]}")
        else:
            replaced_codes.append("-")
    
    return ', '.join(replaced_codes)

# Read the Excel file
df = pd.read_excel('/Users/JoaoAmaral/Documents/Code/procGroup/procGroup.xlsx', sheet_name="Sheet1")
equivalents_df = pd.read_excel('/Users/JoaoAmaral/Documents/Code/procGroup/procGroup.xlsx', sheet_name="Sheet2")

# Create a mapping from the equivalent codes to the original codes
equivalents_map = dict(zip(equivalents_df['similar_inter_code'], equivalents_df['inter_code']))

# Convert all relevant columns to string
df['inter_procedure_code'] = df['inter_procedure_code'].astype(str)
df['bbp_name'] = df['bbp_name'].fillna('').astype(str)
df['Procedure Name'] = df['Procedure Name'].fillna('').astype(str)

# Apply the get_equivalent_string function to create the 'similar_codes' column
df['similar_codes'] = df['inter_procedure_code'].apply(get_equivalent_string)

# Filter out rows where 'similar_codes' contains only '-' characters
df = df[df['similar_codes'].apply(lambda x: x != '-' and not x.replace(' ', '').replace('-', '').isalpha())]

# Group by 'Case ID' and aggregate the 'inter_procedure_code', 'similar_codes', 'bbp_name', and 'Procedure Name' columns into sorted tuples
grouped_code = df.groupby('Case ID')['inter_procedure_code'].apply(lambda x: tuple(sorted(x))).reset_index()
grouped_similar_codes = df.groupby('Case ID')['similar_codes'].apply(lambda x: tuple(sorted(x))).reset_index()
grouped_bbp_name = df.groupby('Case ID')['bbp_name'].apply(lambda x: tuple(sorted(x))).reset_index()
grouped_procedure_name = df.groupby('Case ID')['Procedure Name'].apply(lambda x: tuple(sorted(x))).reset_index()

# Merge grouped dataframes on 'Case ID'
merged_grouped = pd.merge(grouped_code, grouped_bbp_name, on='Case ID')
merged_grouped = pd.merge(merged_grouped, grouped_procedure_name, on='Case ID')
merged_grouped = pd.merge(merged_grouped, grouped_similar_codes, on='Case ID')

# Group by the sorted tuple of 'inter_procedure_code' to get the Case IDs that share them
case_id_groups = merged_grouped.groupby('inter_procedure_code').agg({
    'Case ID': list,
    'bbp_name': 'first',
    'Procedure Name': 'first',
    'similar_codes': 'first'
}).reset_index()

# Filter out the groups that have only one 'Case ID'
shared_case_ids = case_id_groups[case_id_groups['Case ID'].apply(len) > 1]


shared_case_ids.to_excel('testFullV5.xlsx', index=False)
print("done")
