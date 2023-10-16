import pandas as pd

# Read the Excel file
df = pd.read_excel('procGroup.xlsx', sheet_name='Sheet1')

# Convert NaN values to an empty string in relevant columns
df['bbp_name'] = df['bbp_name'].fillna('').astype(str)
df['Procedure Name'] = df['Procedure Name'].fillna('').astype(str)

# Group by 'Case ID' and aggregate the 'inter_procedure_code' and 'bbp_name' columns into sorted tuples
grouped_code = df.groupby('Case ID')['inter_procedure_code'].apply(lambda x: tuple(sorted(x))).reset_index()
grouped_name = df.groupby('Case ID')['bbp_name'].apply(lambda x: tuple(sorted(x))).reset_index()
grouped_procedure_name = df.groupby('Case ID')['Procedure Name'].apply(lambda x: tuple(sorted(x))).reset_index()

# Merge the two grouped dataframes on 'Case ID'
merged_grouped = pd.merge(grouped_code, grouped_name, on='Case ID')
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

shared_case_ids.to_excel('test.xlsx', index=False)
