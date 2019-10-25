dict_months = {'Jan':'01', 'Feb':'02', 'Mar':'03',
               'Apr':'04', 'May':'05', 'Jun':'06',
               'Jul':'07', 'Aug':'08', 'Sep':'09',
               'Oct':'10', 'Nov':'11', 'Dec':'12'}

def DateParser(datestamp):
    
    datestamp_list = datestamp.split(' ')
    
    day = int(datestamp_list[1])
    month = dict_months[str(datestamp_list[2])]
    year = int(datestamp_list[3][:4])  
    
    day = '0' + str(day) if day<10 else str(day)

    return f'{year}-{month}-{day}'

def TimeParser(datestamp):

    datestamp_list = datestamp.split(' ')
    time_long = str(datestamp_list[4])[:-2].split(":")
    
    hour = int(time_long[0])
    minute = str(time_long[1])
    
    if str(datestamp_list[4])[-2:] == 'pm': hour += 12
    hour = '0' + str(hour) if hour<10 else str(hour)

    return f'{hour}:{minute}'