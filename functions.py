import pandas as pd

def write_to_excel_file(list_of_df):
    """

    list_of_df: A python list of tuples in the format [ (<dataframe>, <sheet name>)... ]
    """
    excel_file = pd.ExcelWriter('output.xlsx')
    for df, sheet_name in list_of_df:
        df.to_excel(excel_file, sheet_name=sheet_name, index=False)
    excel_file.save()
    excel_file.close()
