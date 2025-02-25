from datetime import datetime
import numpy as np 
import pandas  as pd 
import os
import matplotlib.pyplot as plt
import seaborn as sns   
# from FeatureExtract import path_check

# ------------------------------------------ STEP TWO 
data_set={0:'logon.csv',1:'device.csv',2:'email.csv',3:'http.csv',4:'file.csv',5:'psychometric.csv'}


# TODO 
def feature_extract():
    """
    """
    pass
# TODO
# Role Analysis

def path_check(path):
    """ Check the path
    """
    folders=os.path.exists(path)
    if not folders:
        print("Create new folders: ' %s ' successfully!"%(path))
        os.makedirs(path)
    else:
        print("The folder  ' %s ' exits, Some data will be rewrited !"%(path))
        pass 
        # os._exit(0)

# DONE 

def new_log(file_in,file_out):
    """ delete the id in the first column
    """
    file_in=open(file_in,'r')
    file_out=open(file_out,'wt')
    for line in file_in:
        line=line.split(',')
        if MACHINE in line:
            newline=','.join(line[1:])
            file_out.writelines(newline)
    file_in.close()

def combine_time_log(file_in,file_out):
    """combine data in the same day

    file_in: the new log data in new folder 
    """
    files_in=open(file_in,'r')
    date_set=['null']
    for line in files_in:
        line=line.split(' ')
        if line[0] not in date_set:
            date_set.append(line[0])
    # print (date_set)
    files_in.close()

    i=0
    files_in=open(file_in,'r')
    files_out=open(file_out,'wt')
    newline=''
    for line in files_in:
        line=line.strip()
        line=line.replace(' ',',')
        if date_set[i] in line:
            newline=newline+' ; '+line
            # print(1)
        else:
            files_out.writelines(newline+'\n')
            newline=line
            i=i+1

def find_weekday(time):
    """ find weekdays for time_two from time_one in weekday: day_one

    Arg:
     time: for example, 01/04/2010
    Return:
     weekday: 1:Monday 2:Tuesday ...
    """
    week=datetime.strptime(time,'%m/%d/%Y').weekday()+1
    return (week)
    
def count_time(time_logon,time_logoff):
    """count the logoning time 

    Arg:
     time_longon: for example, 07:20:00
     time_logoff: for example, 15:20:00
    return:
     last_time: float, the number of hours of online.
    """
    time_logon=datetime.strptime(time_logon,'%H:%M:%S')
    time_logoff=datetime.strptime(time_logoff,'%H:%M:%S')
    last_time=(time_logoff-time_logon).total_seconds()/3600
    last_time=round(last_time,2)
    return last_time
    # print(last_time)
    # print(type(last_time))

# ----------------- 单个用户不同日志特征分析 (Log features for different logs of one user)：
def log_feature(file_input):
    """ logon features from users

    file_input: logon2.csv of users
    """
     

    files_in=open(file_input,'r')
    data_dicts={}
    m=1
    for line in files_in:
        # print (m)
        m=m+1
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # ----- Week
            weekday=find_weekday(week_time)
            # ----- The total number of logon machines 
            computer_number=1
            # ------------     (First Machine, In One day )--------------
            # -----   (the id of the Machine)
            computer_id=1
            # -----   (number of logon in One day  )
            numebr_logon=line.count('Logon')
            # 
            line=line.split(' ; ')
            # -----   (the firt time of logon)
            first_logon=line[0].split(',')[1] # format: 07:20:00
            first_logoff=line[1].split(',')[1]
            first_logon_time=datetime.strptime(first_logon,'%H:%M:%S') 
            first_logoff_time=datetime.strptime(first_logoff,'%H:%M:%S')
            first_logon_hour=first_logon_time.hour
            first_logon_minutes=first_logon_time.minute
            first_logoff_hour=first_logoff_time.hour
            first_logoff_minutes=first_logoff_time.minute
            # print(first_logoff_hour)

            # -----   (the last time of logon)
            last_logon=line[-2].split(',')[1]
            last_logoff=line[-1].split(',')[1]
            last_logon_time=datetime.strptime(last_logon,'%H:%M:%S') 
            last_logoff_time=datetime.strptime(last_logoff,'%H:%M:%S')
            last_logon_hour=last_logon_time.hour
            last_logon_minutes=last_logon_time.minute
            last_logoff_hour=last_logoff_time.hour
            last_logoff_minutes=last_logoff_time.minute
        
            # -----    (the lasting time for a logon = last_logoff - first_logon)
            online_time=count_time(first_logon,last_logoff)
            data_list=[numebr_logon,first_logon_hour,first_logon_minutes,first_logoff_hour,first_logoff_minutes,last_logon_hour,last_logon_minutes,last_logoff_hour,last_logoff_minutes,online_time]
            data_dicts[week_time]=data_list
            # 
    # file_output.writelines(str(data_dicts))
    files_in.close()
    # file_output.close()
    return data_dicts

def device_feature(file_input,log_dicts):
    """ devices feartures

    file_input: device2.csv of users
    """
    files_in=open(file_input,'r')
    m=0
    for line in files_in:
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # -----   (week)
            weekday=find_weekday(week_time)
            # -----   (number of machines that have been connected with devices)
            computer_number=1
            # -----------------------  (the firt machine, in one day)---------------------------
            # -----   (the id of the machine)
            computer_id=1
            # -----   (how many times in using devices in this machine)
            numebr_use_device=line.count('Connect')
           
            data_device=[numebr_use_device]

            log_dicts[week_time]=log_dicts[week_time]+data_device
            # print (log_dicts[week_time])
            # exit(0)
    files_in.close()
    return log_dicts

def email_feature(file_input,http_dicts):
    """ email features
    file_inout: email2.csv of users

    features are marked with : '-----' in the comments 
    """
    files_in=open(file_input,'r')
    for line in files_in:
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # -----   (Week)
            weekday=find_weekday(week_time)
            #
            line=line.split(' ; ')
            # -----   (number of emailing)：
            Number_email=len(line)
            #
            data_email=[]
            for i in range(len(line)):
                eamil_set=[]
                new_line=line[i].replace(';',',')
                new_line=new_line.split(',')
                for string in new_line:
                    # print(string)
                    if '@' in string and (string not in eamil_set):
                        eamil_set.append(string)
                # -----  ：
                Number_receiver=len(eamil_set)-1
                #  ：
                source_email=eamil_set[-1]
                # -----  
                if '@dtaa.com' in source_email:
                    source_email_type=0
                else:
                    source_email_type=1
                receiver_email=eamil_set[:-1]
                Number_company_email=0
                for address in receiver_email:
                    if '@dtaa.com' in address:
                        Number_company_email+=1
                # ----- 每次收件人邮箱为公司邮箱的个数
                # ----- 每次收件人邮箱为私人邮箱的个数
                Number_private_email=Number_receiver-Number_company_email
                # 发件人邮箱所在的索引值（第一次出现）
                source_email_index=new_line.index(source_email)
                # 邮件大小的索引值
                size_index=source_email_index
                while not new_line[size_index].isdigit():
                    size_index=size_index+1
                # ----- 每次邮件大小: （KB）
                size_email=round(float(new_line[size_index])/1024,2)
                # 附件值的索引值
                attachment_index=size_index+1
                # ----- 每次附件的个数:
                attachment_count=int(new_line[attachment_index])

                # 数据拼接
                data_email=data_email+[Number_receiver,source_email_type,Number_company_email,Number_private_email,size_email,attachment_count]
            # print(len(data_email[:24])) 
            # http_dicts[week_time]=http_dicts[week_time]+[weekday,Number_email]+data_email[:24]
            # ----- delete weekday from up
            http_dicts[week_time]=http_dicts[week_time]+[Number_email]+data_email[:24]
            

                # print(source_email)
                # print(Number_receiver)
                # print(Number_company_email)
                # print(Number_private_email)
                # print(log_dicts)
            # exit(0)
    files_in.close()
    # print(log_dicts)
    return http_dicts

# TODO ----------
def file_feature(file_input):
    """ file features 
     (this part is not considered now because of the lack of related data )
    file_input: file2.csv
    """
    files_in=open(file_input,'r')
    for line in files_in:
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # ----- 星期几
            weekday=find_weekday(week_time)
            # 访问文件的次数
    files_in.close()

def http_feature(file_input,device_dicts):
    """ network feature 

    file_input: http2.csv 
    """
    files_in=open(file_input,'r')
    for line in files_in:
        if line !='\n':
            line=line.strip()
            time_line=line.split(',')
            week_time=time_line[0] # format: 01/04/2010
            # ----- 星期几 (week)
            weekday=find_weekday(week_time)
            # 
            line=line.split(' ; ')
            # ----- 访问网页的总次数 (the number of web browsing )
            Numeber_webs=len(line)
            # TODO ----------------访问网页的所有时间汇总 (the information of browsing webpages in different time)-----------
            # time_sets=[]
            # time_hour_sets=[]
            # for i in range(Numeber_webs):
            #     new_line=line[i]
            #     new_line=new_line.split(',')
            #     time_line=new_line[1]
            #     time_sets.append(time_line)
            # for each_time in time_sets:
            #     time_hour=datetime.strptime(each_time,'%H:%M:%S').hour
            #     time_hour_sets.append(time_hour)
            # TODO -------- 访问网页的时间段分布 ————可以较好的模拟出一个人的行为习惯，可以用于检测出是否非本人登录。———— 但是在本次数据中，不建议采用，因为不存在如此的情况。 (the record of browsing webpages in different time will provide useful information in simulating a users' habbit in browsing webpages. And it will be useful to detect illegal logon.  )
            # --8:00
            # time_brefore=time_hour_sets.count(7)+time_hour_sets.count(6)+time_hour_sets.count(5)+time_hour_sets.count(4)
            # # 8-9
            # time_One=time_hour_sets.count(8)
            # # 9-10
            # time_Two=time_hour_sets.count(9)
            # # 10-11
            # time_Three=time_hour_sets.count(10)
            # # 11-12
            # time_Four=time_hour_sets.count(11)
            # # 12-13
            # time_Five=time_hour_sets.count(12)
            # # 13-14
            # time_Six=time_hour_sets.count(13)
            # # 14-15
            # time_Seven=time_hour_sets.count(14)
            # # 15-16
            # time_Eight=time_hour_sets.count(15)
            # # 16-17
            # time_Nine=time_hour_sets.count(16)
            # # 17-18
            # time_Ten=time_hour_sets.count(17)
            # # 18-19
            # time_Eleven=time_hour_sets.count(18)
            # # 19:00 --
            # time_Twelve=time_hour_sets.count(19)+time_hour_sets.count(20)+time_hour_sets.count(21)+time_hour_sets.count(22)+time_hour_sets.count(23)
            # --------------------------------------------------------------------

            # print (time_hour_sets)
            # print(time_Four)

            # 数据拼接
            # data_http=[weekday,Numeber_webs]
            #----- delete weekday from up
            data_http=[Numeber_webs]
            device_dicts[week_time]=device_dicts[week_time]+data_http

    files_in.close()
    return device_dicts
            # exit(0)

def dict_complemetion(dicts,set_length):
    for (key,value) in dicts.items():
        while len(value)<set_length:
            value.append(0)
    return dicts

def mix_complemention(dicts,columns,set_length):
    """
    对输入的dicts 数据维度进行统一，dicts 的value中有两个list,columns=0时 操作第一个lists；colums=1时操作第二个lists
    """
    for (key,value) in dicts.items():
        while len(value[columns])<set_length:
            value[columns].append(0)
    return dicts

# ---------------------------- temp 
def list_complemetion(lists,set_length):
    while len(lists)<set_length:
        lists.append(0)
    return lists

def file_sequence(file_in,file_type):
    """
    generate the sequence according to date
     Arg:
      file_in:
      file_type: int (0-4, 0:logon, 1:device, 2:email, 3:file, 4:http)
     Return:
      a dict of sequences, key: date; value: actions and time.
    """

    type_set={0:'logon', 1:'device', 2:'email', 3:'file', 4:'http'}
    type_words=type_set[file_type]
    files_in=open(file_in,'r')
    sequences_set={}
    for line in files_in:
        if line !='\n':
            line=line.split(' ; ')
            # print (len(line))
            for records in line:
                if file_type==0 and 'Logon'in records:
                    type_words= 'logon'
                elif file_type==0 and 'Logoff'in records:
                    type_words= 'logoff'
                if file_type==1 and 'Connect' in records:
                    type_words= 'Connect'
                elif file_type==1 and 'Disconnect' in records:
                    type_words='Disconnect'
                records=records.split(',')
                if records[0] in sequences_set:
                    # 同一天的不同时刻记录拼接
                    values=records[1]+'#'+type_words
                    sequences_set[records[0]]=sequences_set[records[0]]+' & '+values
                else:
                    values=records[1]+'#'+type_words
                    sequences_set[records[0]]=values
    files_in.close()
    return(sequences_set)

def sequence_combine(sequence_one,sequence_two):
    """
    combine two sequence dicts according to key (date).
     Arg:
      sequence_one: dicts
      sequence_two: dicts 
     Return: a combined dict.
    """

    for (date,record) in sequence_two.items():
        if date in sequence_one:
            new_record=sequence_one[date]+' & '+record
            sequence_one[date]=new_record
        else:
            print ('some date missed! Please change the combination order')
            exit(0)
        # print(sequence_one)
        # exit(0)
    return(sequence_one)
    # return(sequence_one)
     
def sort_actions_One_Day(Day_records):
    """
    sort actions in One day through time.
        Arg：
         Day_records: a string composed of time and actions (08:56:00#logon & 17:05:00#logoff...)
        Return: a string of sorted sequence of actions. 
    """
    line=Day_records.split(' & ')
    length=len(line)
    actions_dict={}
    time_dict=[]
    actions_sorted=[]
    for temp_data in line:
        # temp_data[0:8] 为时间数据， temp_data[9:]为行为数据，其中中间丢弃了‘#’符号
        actions_dict[temp_data[0:8]]=temp_data[9:]
        time_dict.append(temp_data[0:8])
    time_sorted=quick_sort_datetime(time_dict)
    for time_string in time_sorted:
        actions_sorted.append(actions_dict[time_string])
    action_sequence=','.join(actions_sorted)
    return action_sequence,length

def sort_actions_InSequence(sequence_in,save_file):
    """
    sort actions day by day in the dict through time.
     Arg:
      sequence_in: a dict (the disordered sequence)
     Return: a dict (the ordered sequence)
    """ 
    files=open(save_file,'wt')
    max_length=0
    for (date,records) in sequence_in.items():
        actions_sequence,day_actions_length=sort_actions_One_Day(records)
        files.writelines(date+' : '+actions_sequence+'\n')
        if day_actions_length>max_length:
            max_length=day_actions_length
    print( USERNAME,'_maxlength: ',max_length)
    return max_length

def quick_sort(array):
    """
    quick sort algorithm
        Arg:
         array: a list 
        Return: a list
               
    """
    smaller_list=[]
    bigger_list=[]
    equal_list=[]
    if len(array)<=1:
        return array
    else:    
        middle_key=array[0]
        for records in array:
            if records < middle_key:
                smaller_list.append(records)
            elif records > middle_key:
                bigger_list.append(records)
            else:
                equal_list.append(records)
        smaller_list=quick_sort(smaller_list)
        bigger_list=quick_sort(bigger_list)
        return smaller_list+equal_list+bigger_list

def quick_sort_datetime(array):
    """
    quick sort algorithm for datetime class.
     Arg:
         array: a list (elements belong to datetime class)
     Return: a list (elements belong to string)
    """
    smaller_list=[]
    bigger_list=[]
    equal_list=[]
    if len(array)<=1:
        return array
    else:    
        middle_key=datetime.strptime(array[0],'%H:%M:%S')
        for records in array:
            datetime_records=datetime.strptime(records,'%H:%M:%S')
            if datetime_records < middle_key:
                smaller_list.append(records)
            elif datetime_records > middle_key:
                bigger_list.append(records)
            else:
                equal_list.append(records)
        smaller_list=quick_sort(smaller_list)
        bigger_list=quick_sort(bigger_list)
        return smaller_list+equal_list+bigger_list

def sequence_code(sequence_files_in,sequence_code_save,sequence_len):

    code_dict={'logon':1,'Connect':2,'Disconnect':3,'http':4,'email':5,'logoff':6}
    file_in=open(sequence_files_in,'r')
    file_out=open(sequence_code_save,'wt')
    file_out.close()
    file_out=open(sequence_code_save,'a+')
    for line in file_in:
        line=line.strip()
        line=line.split(' : ')
        week_day=find_weekday(line[0])
        sequences=line[1].split(',')
        sequence_codes=[]
        for actions in sequences:
            sequence_codes.append(code_dict[actions])
        sequence_codes=list_complemetion(sequence_codes,sequence_len)
        sequence_codes=np.reshape(sequence_codes,(1,sequence_len))
        np.savetxt(file_out,sequence_codes,fmt='%f',delimiter=',')
    file_out.close()

# ------------------------------------------


# --------- preprocessing (logon.csv, device.csv ...)
def pre_step():
    """
      data preprocessing 
    """
    path='Data/'+USERNAME+'/new'
    path_check(path)
    filetype=['/http.csv','/device.csv','/email.csv','/file.csv','/http.csv','/logon.csv']
    for type_num in range (len(filetype)):
        new_log('Data/'+USERNAME+filetype[type_num],path+filetype[type_num])

    # step 2  ----------- combine data in the same day 
    new_filename=['/http2.csv','/device2.csv','/email2.csv','/file2.csv','/http2.csv','/logon2.csv']
    for type_num in range (len(filetype)):
        file_in='Data/'+USERNAME+'/new'+filetype[type_num]
        file_out='Data/'+USERNAME+'/new'+new_filename[type_num]
        combine_time_log(file_in,file_out)
# # ---------------------------------------------------------------
def create_bar_plot(activity_type, ylabel, color):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(activity_counts[activity_type].keys()), 
                y=list(activity_counts[activity_type].values()), 
                palette=color)
    plt.title(f"{activity_type.capitalize()} Activity per User")
    plt.xlabel("User")
    plt.ylabel(ylabel)
    plt.grid(axis="y")
    plt.show()

# ✅ Function to create pie charts
def create_pie_chart(activity_type):
    plt.figure(figsize=(7, 7))
    data = activity_counts[activity_type]
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title(f"{activity_type.capitalize()} Activity Distribution")
    plt.show()

# ✅ Function to create heatmaps
def create_heatmap():
    df = pd.DataFrame(activity_counts)
    plt.figure(figsize=(8, 6))
    sns.heatmap(df.T, annot=True, cmap="coolwarm", fmt="d")
    plt.title("User Activity Heatmap")
    plt.xlabel("Users")
    plt.ylabel("Activity Type")
    plt.show()

# ✅ Function to create histograms for logon times
def plot_login_histogram():
    plt.figure(figsize=(10, 5))
    
    for user in user_folders:
        logon_file = os.path.join(base_path, user, "new", "logon.csv")
        if os.path.exists(logon_file):
            df = pd.read_csv(logon_file)
            times = pd.to_datetime(df.iloc[:, 1], format="%H:%M:%S").dt.hour
            sns.histplot(times, bins=24, kde=True, label=user, alpha=0.6)
    
    plt.title("Logon Time Distribution")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()
# ----------- feature generating 
def Feature_generate(file_in,file2_in,file3_in,file4_in):
    """
    Generate features for every user
    """
    path_feature='Data/'+USERNAME+'/feature'
    path_check(path_feature)
    file_out='Data/'+USERNAME+'/feature/data_out.csv'
    log_dicts=log_feature(file_in)
    device_dicts=device_feature(file2_in,log_dicts)
    # -------- original
    new_device_dicts=dict_complemetion(device_dicts,11)
    # --------- change 
    # new_device_dicts=dict_complemetion(device_dicts,20)
    # ----- end
    http_dicts=http_feature(file4_in,new_device_dicts)
    # -------- original
    new_http_dicts=dict_complemetion(http_dicts,12)
    # --------- change 
    # new_http_dicts=dict_complemetion(http_dicts,22)
    # ----- end
    email_dicts=email_feature(file3_in,new_http_dicts)
    # new_email_dicts=dict_complemetion(email_dicts,41)
    new_email_dicts=dict_complemetion(email_dicts,37)
    # 数据清空 (empty the file)
    data_save=open(file_out,'wt')
    data_save.close()
    # 数据保存 (save data )
    data_save=open(file_out,'a+')
    for (key,value) in new_email_dicts.items():
        # print (len(value))
        values=np.reshape(value,(-1,37))
        np.savetxt(data_save,values,fmt='%f',delimiter=',')
    data_save.close()

#-------------------------------------------
def Sequence_generate(file_in,file2_in,file3_in,file4_in):
    """
    Generate action sequences for every user
    """
    path='Data/'+USERNAME+'/sequence'
    path_check(path)
    ActionSeq_save_path='Data/'+USERNAME+'/sequence/actions_sequence.csv'
    sequence_temp='Data/'+USERNAME+'/sequence/sequence_temp.csv'
    sequence_code_save='Data/'+USERNAME+'/sequence/sequence_code.csv'

    logon_time_sequence=file_sequence(file_in,0)
    device_time_sequence=file_sequence(file2_in,1)
    email_time_sequence=file_sequence(file3_in,2)
    http_time_sequence=file_sequence(file4_in,4)

    Final_Sequence=sequence_combine(logon_time_sequence,device_time_sequence)
    Final_Sequence=sequence_combine(Final_Sequence,email_time_sequence)
    Final_Sequence=sequence_combine(Final_Sequence,http_time_sequence)
    max_length=sort_actions_InSequence(Final_Sequence,ActionSeq_save_path)

    file_temp=open(sequence_temp,'wt')
    file_temp.writelines(str(Final_Sequence))
    file_temp.close()
    # -------------- sequence code (特征数字化)    
    sequence_code(ActionSeq_save_path,sequence_code_save,max_length)

    # --------------------------

def create_bar_plot(activity_type, ylabel, color):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(activity_counts[activity_type].keys()), 
                y=list(activity_counts[activity_type].values()), 
                palette=color)
    plt.title(f"{activity_type.capitalize()} Activity per User")
    plt.xlabel("User")
    plt.ylabel(ylabel)
    plt.grid(axis="y")
    plt.show()
if __name__ == "__main__":
    # EDB0714--PC-6103  HXL0968--PC-0623  TNM0961--PC-2030
    # user_sets=['HXL0968'] #'HXL0968'
    # MACHINE='PC-0623'
    # for username in user_sets:
    #     USERNAME=username
# Set base directory where the user folders are located

    user_sets={'EDB0714':'PC-6103','HXL0968':'PC-0623','TNM0961':'PC-2030'}
    for username,machine in user_sets.items():
        USERNAME=username
        MACHINE=machine
        # print(USERNAME)
        file_in ='Data/'+USERNAME+'/new/logon2.csv'
        file2_in='Data/'+USERNAME+'/new/device2.csv'
        file3_in='Data/'+USERNAME+'/new/email2.csv'
        file4_in='Data/'+USERNAME+'/new/http2.csv'

        # preprocessing 
        pre_step()
        # generate the feature for daily behaviors.
        Feature_generate(file_in,file2_in,file3_in,file4_in)
        # generate the sequence data for daily action sequences.
        Sequence_generate(file_in,file2_in,file3_in,file4_in)



    base_path = "Data"

    # Define user folders
    user_folders = ["EDB0714", "HXL0968", "TNM0961"]

    # Initialize dictionaries to store data counts
    activity_counts = {
        "logon": {},
        "device": {},
        "email": {},
        "file": {},
        "http": {}
    }
    for user in user_folders:
     user_path = os.path.join(base_path, user, "new")
    # Generate bar plots for each activity type 
    # Define file paths for different activity types
     files = {
        "logon": os.path.join(user_path, "logon.csv"),
        "device": os.path.join(user_path, "device.csv"),
        "email": os.path.join(user_path, "email.csv"),
        "file": os.path.join(user_path, "file.csv"),
        "http": os.path.join(user_path, "http.csv")
     }
    
    # Count occurrences in each CSV file
     for key, file in files.items():
        if os.path.exists(file):
            activity_counts[key][user] = sum(1 for line in open(file)) - 1  # Excluding header
        else:
            activity_counts[key][user] = 0  # If file doesn't exist, set count to 0




   

    create_bar_plot("logon", "Logon Events", "Blues_r")
    create_bar_plot("device", "Device Connections", "Greens_r")
    create_bar_plot("email", "Emails Sent/Received", "Purples_r")
    create_bar_plot("file", "Files Accessed", "Oranges_r")
    create_bar_plot("http", "Websites Visited", "Reds_r")

    create_pie_chart("logon")
    create_pie_chart("device")
    create_pie_chart("email")

    create_heatmap()
    plot_login_histogram()