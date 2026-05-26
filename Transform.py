import pandas as pd, datetime as dt,os

class transform():
  def __init__(self,data,location,machine_id,document_type,output_path,start_date=None,end_date=None) -> None:
      self.data = data
      self.location = location
      self.machine_id = machine_id
      self.document_type = document_type
      self.output_path = output_path
      self.start_date = start_date
      self.end_date = end_date
      self.file_name = None
      self.files_name = []

  def transform(self):
      start_date = pd.Timestamp(self.start_date)
      end_date = pd.Timestamp(self.end_date)
      df = self.data.loc[self.data["location"]== self.location]
      df['datetime'] = pd.to_datetime(df['datetime'])
      df['date'] = pd.to_datetime(df['date']).dt.date
      df["hourly"] = df["datetime"].dt.strftime('%H').astype(int)
      df_pivot = df.pivot_table(index=['date','hourly'], values=['net_sales',"order_number"], aggfunc={'net_sales': 'sum', 'order_number': pd.Series.nunique}, fill_value=0).reset_index()
      df_pivot_sorted = df_pivot.sort_values(by=["date", "hourly"], ascending=[False, False])
      hour_24 = pd.DataFrame({'hourly': range(0, 24)})
      date_range = pd.date_range(start=start_date, end=end_date, freq='D')
      hour_24 = pd.concat([hour_24.assign(date=date) for date in date_range], ignore_index=True)
      hour_24["date"] = pd.to_datetime(hour_24.date).dt.date
      df_new = pd.merge(hour_24,df_pivot_sorted,on=["date","hourly"],how="left").fillna(0)
      df_new["machine_id"] = self.machine_id
      df_new["Batch ID"] = pd.to_datetime(df_new["date"]).dt.strftime('%Y%m%d')
      df_new["Date"] = pd.to_datetime(df_new["date"]).dt.strftime('%d%m%Y')
      df_new["hourly"] = df_new["hourly"].apply(lambda x: '{:02d}'.format(int(x)))
      df_new["net_sales"] = df_new["net_sales"].apply(lambda x: '{:.2f}'.format(float(x)))
      df_new["Final"] = df_new["machine_id"]+"|"+df_new["Batch ID"]+"|"+df_new["Date"]+"|"+df_new["hourly"].astype(str)+"|"+df_new["order_number"].round(0).astype(int).astype(str)+"|"+df_new["net_sales"]+"|0.00|0.00|0.00|0|"+df_new["net_sales"]+"|0.00|0.00|0.00|0.00|0.00|0.00|Y"
      df_new["File"]="H"+self.machine_id+"_"+df_new["Batch ID"]
      return df_new[["File","Final"]]

  def transform_24(self):
      df_new = self.transform()
      os.chdir(self.output_path)
      for i in df_new["File"].unique():
        df_new.loc[df_new["File"]==i]["Final"].to_csv("{}.txt".format(i),index=False,header=False)
        self.file_name=i+'.txt'
        self.files_name.append(self.file_name)
        print(self.file_name,"...Done")


  def by_day(self):
      # Create a new 'date' column
      data = self.data.loc[self.data["location"] == self.location]
      data["date"] = '{}{}'.format(self.document_type, self.machine_id) + pd.to_datetime(data.date).dt.strftime('%Y%m%d')
      data["file_name"] = '{}{}'.format(self.document_type, self.machine_id)
      data_grouped = pd.DataFrame(data.groupby(['date','file_name']).sum('net_sales').reset_index())

      # Round 'total_price' to 2 decimal places and format as string
      data_grouped["net_sales"] = data_grouped["net_sales"].round(2).map("{:.2f}".format)

      # Extract lengths of integer and fractional parts
      data_grouped["lenfront"] = data_grouped['net_sales'].apply(lambda x: len(str(x).split('.')[0]) if '.' in str(x) else 0)
      data_grouped["lenback"] = data_grouped['net_sales'].apply(lambda x: len(str(x).split('.')[1]) if '.' in str(x) else 0)

      # Extract the integer part as 'test'
      data_grouped["test"] = data_grouped['net_sales'].apply(lambda x: str(x).split('.')[0])

      # Pad '0' to the left and right to achieve desired lengths
      data_grouped['0_'] = data_grouped['lenfront'].apply(lambda x: '0'.zfill(8 - x))
      data_grouped['_0'] = data_grouped['lenback'].apply(lambda x: '0'.zfill(2 - x) if 2 - x != 0 else '')

      # Create the 'final' column
      data_grouped['final'] = data_grouped['date'] + data_grouped['0_'] + data_grouped['net_sales'].astype(str) + data_grouped['_0']

      return data_grouped[['file_name','final']]

  def series(self,files=None):
      final = self.by_day()
      os.chdir(self.output_path)

      existing = len(os.listdir(os.getcwd()))
      if files == None: files = existing
      else: files = files + existing

      for i,j in zip(range(files,final["final"].count()+files),final["final"]):
        self.file_name = self.document_type+self.machine_id+"."+str(i).zfill(3)+".txt"
        final["final"].loc[ final["final"] == str(j)].to_csv(self.file_name,index=False, header=False)
        self.files_name.append(self.file_name)
        print(self.file_name+"...Done")

  def API_Transform(self):
        df = self.data.copy()
        df = df.loc[df["location"]==self.location].groupby(['order_number','datetime','date','location']).sum().reset_index().copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.loc[(df['date']>=self.start_date) & (df['date']<=self.end_date)]
        df['ReceiptNo'] = df['order_number'].map(lambda x:'#'+str(x))
        df['SubTotal'] = df['net_sales']
        df['DiscountPercent'] = 0.0
        df['DiscountAmount'] = 0.0
        df['GstPercent'] = 0.0
        df['GstAmount'] = 0.0
        df['ServiceChargePercent'] = 0.0
        df['ServiceChargeAmount'] = 0.0
        df['GrandTotal'] = df['net_sales']
        df['IsTest'] = False
        df['IsVoid'] = False
        df['ReceiptDateAndTime2'] = df['datetime']
        df = df.drop(['datetime','date','order_number','net_quantity','net_sales','location'],axis=1)
        df.to_csv(f'{self.output_path}/BU2_{self.start_date}_{self.end_date}.csv',index=False)
        print("Receipt Sended: ",len(df),f" from {self.start_date} to {self.end_date}")
        return df