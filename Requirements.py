import datetime as dt,os
today = dt.date.today()
yesterday = dt.date.today() - dt.timedelta(days=1)
twodaysago = dt.date.today() - dt.timedelta(days=2)
path = os.path.dirname(os.path.abspath(__file__))

List_to_run = ['BKE','BIP','PGP','EMP','BU2','BMA'] # ['BMA']#'PGP','ASP','EMP'

gen_dic = {
    "start" :
                '2026-05-29'
                #f'{yesterday}'
    ,"end"  :
                '2026-05-29'
                #f'{yesterday}'
}

# sftp://
all_outlet = {

'BKE_dic' : {
    "location":"BKE",
    "machine_id":"7500218",
    "document_type":"D",
    "file_start":797 + (yesterday - dt.date(2026,5,26)).days,
    "output_path":f"{path}/BKE",
    "sftp_client":{
        "hostname":'isendit.capitaland.com',
        "port":2222,
        "username":'dts_pos7500218_p',
        "password":'3w*Q^2M!n1'
    },
        "remote_folder_path":'POS/75/7500218'
},

#New PGP
'PGP_dic' : {
    "location":"PGP",
    "machine_id":"7000729",
    "document_type":"D",
    "file_start":737 + (yesterday - dt.date(2026,5,26)).days,
    "output_path":f"{path}/PGP",
    "sftp_client":{
        "hostname":'20.195.109.4',
        "port":2222,
        "username":'dts_pos7000729_p',
        "password":'Km0^1*Ms!3'
    },
    "remote_folder_path":'POS/70/7000729'
},

#Old PGP
# 'PGP_dic' : {
#     "location":"PGP",
#     "machine_id":"7000038",
#     "document_type":"D",
#     "output_path":f"{path}/PGP",
#     "sftp_client":{
#         "hostname":'20.195.109.4',
#         "port":2222,
#         "username":'dts_pos7000038_p',
#         "password":'Nm09*&Ws)2'
#     },
#     "remote_folder_path":'/POS/70/7000038'
# },

'EMP_dic' : {
    "location":"EMP",
    "machine_id":"8200020",
    "document_type":"H",
    "output_path":f"{path}/EMP",
    "sftp_client":{
        "hostname":'ftp.phb.com.my',
        "port":22,
        "username":'8200020',
        "password":'aOhwHZT4'
    },
        "remote_folder_path":''
},

'ASP_dic' : {
    "location":"ASP",
    "machine_id":"52000168",
    "document_type":"H",
    "output_path":f"{path}/ASP",
    "sftp_client":{
        "hostname":'sunway.serveftp.org',
        "port":22,
        "username":'52000168',
        "password":'boObfYR'
    },
    "remote_folder_path":''

},

'AIP_dic' : {
    "location":"AIP",
    "machine_id":"30001160",
    "document_type":"H",
    "output_path":f"{path}/AIP",
    "sftp_client":{
        "hostname":'ioimallspos.synthesis.bz',#'1.32.62.138',
        "port":22,
        "username":'30001160',
        "password":'ocL7u4s'
    },
    "remote_folder_path":''

},

'BIP_dic' : {
    "location":"BIP",
    "machine_id":"30000154",
    "document_type":"H",
    "output_path":f"{path}/BIP",
    "sftp_client":{
        "hostname":'ioimallspos.synthesis.bz',#'1.32.62.138',
        "port":22,
        "username":'30000154',
        "password":'28YI6tq'
    },
    "remote_folder_path":''

},

'BMA_dic' : {
    "location":"BMA",
    "machine_id":"7800003",
    "document_type":"D",
    "file_start":701 + (yesterday - dt.date(2026,5,26)).days,
    "output_path":f"{path}/BMA",
    "sftp_client":{
        "hostname":'20.195.109.4',
        "port":2222,
        "username":'dts_pos7800003_p',
        "password":'5Rur3YQ@09'
    },
    "remote_folder_path":'POS/78/7800003'
},

'BU2_dic' : {
    "location":"BU2",
    "machine_id":"",
    "document_type":"API",
    "output_path":f"{path}/BU2",
    "sftp_client":{
        "hostname":'https://tms.1utama.com.my/POS/POSService.svc/SendReceipts',
        "port":0,
        "username":'',
        "password":'Basic RzEyODppMkZ6MnJmM3JwY1Y='
    },
    "remote_folder_path":''

}


}
