import pandas as pd

df = pd.read_excel("sampleData.xlsx")
main_procedures = []
group_arrays = {}
main = []
notMain = []
count = 0

# Group rows by 'case_id'
grouped = df.groupby('Case ID')

for case_id, group in grouped:
    bbp_names = group['bbp_name'].tolist()
    group_arrays[case_id] = bbp_names

for case_id in group_arrays:
    main = []  # Reset 'main' list for each case
    notMain = []  # Reset 'notMain' list for each case
    for procedure in group_arrays[case_id]:
        if 'ECTOMY' in procedure or "EXCISION" in procedure or "RESECTION" in procedure or "DEBULKING" in procedure:
            main.insert(0,procedure)
        elif 'ANASTOMOSIS' in procedure or 'RECONSTRUCTION' in procedure:
            main.append(procedure)
        elif 'OSCOPY' in procedure or "N/F" in procedure:
            notMain.append(procedure)
        else:
            notMain.insert(0,procedure)
    result = main + notMain
    count+=1
    print(result)
print(count)

# # Iterate through each group
# for case_id, group in grouped:
#     # print(f'Case ID: {case_id}')
#     multi_resection = False
#     main_found = False
#     for index, row in group.iterrows():
#         bbp_name = row['bbp_name']
#         # Perform actions with 'bbp_name' for the current 'case_id' group
#         if bbp_name.endswith('ECTOMY'):
#             if multi_resection == False:
#                 multi_resection = True
#                 main_found = True
#                 main_procedures.append(bbp_name)
                           
            
#             # print(main_procedures)
        # print(f'bbp_name: {bbp_name}')


    

# def main_procedure(procedure_groups):
#     main_procedures = []
#     for group in procedure_groups:
#         individual_procedures = [proc.strip() for proc in group.split(',')]  # Split the string into individual procedures
#         main = [proc for proc in individual_procedures if proc.endswith('ECTOMY') or 'RESECTION' in proc]
#         if main:
#             main_procedures.append(main[-1])
#         else:
#             non_main = [proc for proc in individual_procedures if proc.endswith('OSCOPY')]
#             remaining = [proc for proc in individual_procedures if proc not in non_main and proc != 'N/F']
#             if remaining:
#                 main_procedures.append(remaining[-1])
#             else:
#                 main_procedures.append(non_main[-1])
#     return main_procedures

# # Load the Excel file into a DataFrame
# file_path = 'mainProcPy.xlsx'  # Change to your file path
# df = pd.read_excel(file_path, sheet_name="Working")

# # Assuming the procedure data is in a column named 'ProcedureColumn'
# procedure_groups = df['groups']

# # Apply the main_procedure function to the data
# result = [main_procedure(group) for group in procedure_groups]

# # Add the result as a new column in the DataFrame
# df['MainProcedure'] = result

# # Save the modified DataFrame back to the Excel file
# output_file = 'output_file.xlsx'  # Change 'output_file.xlsx' to your desired output file name
# df.to_excel(output_file, index=False)
