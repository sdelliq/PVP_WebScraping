import pandas as pd

# pd.DataFrame(parsed_data).to_excel('scraped_data.xlsx', index=False) #saves the output normally, without column widht adjusted
def dicToExcel(dics_df):
    with pd.ExcelWriter('scraped_data.xlsx', engine='xlsxwriter') as writer:
        dics_df.to_excel(writer, sheet_name='RisultatiTribunali', index=False)
        worksheet = writer.sheets['RisultatiTribunali']
        # Get the maximum length of data in each column
        for i, col in enumerate(dics_df.columns):
            max_len = max(dics_df[col].astype(str).apply(len).max(), len(col) + 2)
            worksheet.set_column(i, i, max_len)  # Set the column width