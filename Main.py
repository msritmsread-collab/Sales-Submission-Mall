import os
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
import Requirements as req, extract_BQ, pandas as pd, warnings
from Transform import transform
from SFTP import SFTPClient
from Rest_API import API
warnings.filterwarnings('ignore')

# Import Data from Warehouse

os.makedirs("Temp_Data", exist_ok=True)
if not os.path.exists(f"Temp_Data/data_{req.gen_dic['start']}_{req.gen_dic['end']}.csv"):
    BigQuery = extract_BQ.BigQueryHandler(os.path.join(req.path,"BigQuery_Credential.json"))
    df = BigQuery.run_query(f"""
                            SELECT CAST(datetime AS STRING) AS datetime, date, CAST(order_number AS STRING) AS order_number, CAST(net_quantity AS STRING) AS net_quantity, net_sales, location
                            FROM msr-msia-sales-analysis.Report_MSREAD.order_MY
                            WHERE date BETWEEN '{req.gen_dic['start']}' AND '{req.gen_dic['end']}'
                            UNION ALL
                            SELECT CAST(datetime AS STRING) AS datetime, date, CAST(order_number AS STRING) AS order_number, CAST(net_quantity AS STRING) AS net_quantity, net_sales, location
                            FROM msr-msia-sales-analysis.Report_AURI.order_MY
                            WHERE date BETWEEN '{req.gen_dic['start']}' AND '{req.gen_dic['end']}'
                            """)
    df.to_csv(f"Temp_Data/data_{req.gen_dic['start']}_{req.gen_dic['end']}.csv",index=False)
    print("Extract Data from Big Query... Done \n")
df = pd.read_csv(f"Temp_Data/data_{req.gen_dic['start']}_{req.gen_dic['end']}.csv")

# Transform
for i in req.all_outlet.values():
    if i['location'] not in req.List_to_run: continue
    else: pass

    os.makedirs(i['output_path'], exist_ok=True)
    path = i['output_path']

    # Declare Parameter
    data = transform(df,i['location'],i['machine_id'],i['document_type'],i['output_path'],req.gen_dic['start'],req.gen_dic['end'])
    # print(data.by_day()['final'],'\n')
    if i['document_type'] == 'H'    : data.transform_24()
    elif i['document_type'] == 'D'  : data.series(files=i.get('file_start',0))
    elif i['document_type'] == 'API':
        df = data.API_Transform()
        API(df,*i['sftp_client'].values()).API_send()
    else    : continue

    # SFTP Send Latest Files
    if i['document_type'] != 'API':
        print("\nSending...")
        send = SFTPClient(*i['sftp_client'].values())
        send.connect()
        if len(data.files_name) == 1    : send.send_file(i['output_path'],i['remote_folder_path'],data.file_name)
        elif len(data.files_name) > 1   : send.send_files(i['output_path'],i['remote_folder_path'],data.files_name)
        else:   print('No files to send')
    else : continue