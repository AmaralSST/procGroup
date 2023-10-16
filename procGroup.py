import pandas as pd

def replace_with_or(cell):
    cell = str(cell)  # Convert to string just in case there are any float values
    # Split the cell content by comma
    codes = cell.split(',')
    
    codes = [code.strip() for code in codes]
    # Replace the codes using the equivalents_map
    replaced_codes = []
    for code in codes:
        code_stripped = code.strip()
        if code_stripped in equivalents_map:
            replaced_code = f"{code_stripped} OR {equivalents_map[code_stripped]}"
            replaced_codes.append(replaced_code)
        else:
            replaced_codes.append(code_stripped)
    
    # Join the codes back into a single string with comma as the delimiter
    return ','.join(replaced_codes)


# Read the Excel file
df = pd.read_excel('procGroup.xlsx', sheet_name="Sheet1")
equivalents_df = pd.read_excel('procGroup.xlsx', sheet_name="Sheet2")

equivalents_df['similar_inter_code'] = equivalents_df['similar_inter_code'].fillna('').astype(str)
equivalents_df['inter_code'] = equivalents_df['inter_code'].fillna('').astype(str)

# Create a mapping from the equivalent codes to the original codes
equivalents_map = dict(zip(equivalents_df['similar_inter_code'], equivalents_df['inter_code']))

# Update the way we create equivalents_map to handle multiple equivalent codes
equivalents_map = {}
for _, row in equivalents_df.iterrows():
    if row['similar_inter_code']:  # this ensures we're not processing empty values
        equivalents = ' OR '.join(row['similar_inter_code'].split(';'))
        equivalents_map[row['inter_code']] = equivalents

# Apply the function to the inter_procedure_code column
df['inter_procedure_code'] = df['inter_procedure_code'].astype(str).apply(replace_with_or)


# Convert NaN values to an empty string in relevant columns
df['bbp_name'] = df['bbp_name'].fillna('').astype(str)
df['Procedure Name'] = df['Procedure Name'].fillna('').astype(str)

# Group by 'Case ID' and aggregate the 'inter_procedure_code', 'bbp_name' and 'Procedure Name' columns into sorted tuples
grouped_code = df.groupby('Case ID')['inter_procedure_code'].apply(lambda x: tuple(sorted(x))).reset_index()
grouped_bbp_name = df.groupby('Case ID')['bbp_name'].apply(lambda x: tuple(sorted(x))).reset_index()
grouped_procedure_name = df.groupby('Case ID')['Procedure Name'].apply(lambda x: tuple(sorted(x))).reset_index()

# Merge grouped dataframes on 'Case ID'
merged_grouped = pd.merge(grouped_code, grouped_bbp_name, on='Case ID')
merged_grouped = pd.merge(merged_grouped, grouped_procedure_name, on='Case ID')

# Group by the sorted tuple of 'inter_procedure_code' to get the Case IDs that share them
case_id_groups = merged_grouped.groupby('inter_procedure_code').agg({
    'Case ID': list,
    'bbp_name': 'first',
    'Procedure Name': 'first'
}).reset_index()

# Filter out the groups that have only one 'Case ID'
shared_case_ids = case_id_groups[case_id_groups['Case ID'].apply(len) > 1]

print(shared_case_ids)

shared_case_ids.to_excel('testFullV5.xlsx', index=False)


