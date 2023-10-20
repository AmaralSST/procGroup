import pandas as pd

df = pd.read_excel("sampleData.xlsx")
group_arrays = {}

# Group rows by 'Case ID'
grouped = df.groupby('Case ID')

results = []
for case_id, group in grouped:
    main = []
    notMain = []

    for procedure in group['bbp_name']:
        if 'ECTOMY' in procedure or "EXCISION" in procedure:
            main.append(procedure)
        elif 'OSCOPY' in procedure or "N/F" in procedure:
            notMain.append(procedure)
        else:
            main.append(procedure)

    result = main + notMain
    results.append(result[0])  # Add the first result to the results list
    # Add empty lines for the rest of the group
    empty_lines = [''] * (len(group) - 1)
    results.extend(empty_lines)

# Add the 'Result' column to the DataFrame
df['Result'] = results

# Save the modified DataFrame to a new Excel file
df.to_excel("sampleData_with_results.xlsx", index=False)
