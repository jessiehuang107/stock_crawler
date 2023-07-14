# import requests
# url='https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY'
# rq=requests.get(url,params={
#     'response':"json",
#     'stockNO':'2330',
#     'date':'20230713')}

# <stockData>
#   <url>https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY</url>
#   <startYear>2020</startYear>
#   <startMonth>1</startMonth>
#   <endYear>2023</endYear>
#   <endMonth>6</endMonth>
#   <stockNo>2317</stockNo>
# <stockData>

import xml.etree.ElementTree as ET
import requests
import time
from openpyxl import Workbook
def xml_to_dict(element):
    result = {}
    for child in element:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(child)
    return result
def fillSheet(sheet,data,row):#建立一個function名稱裡面放置三種參數sheet,data,row
    for column, value in enumerate(data,1):#讀取資料
        sheet.cell(row = row,column = column,value = value) 
        #將資料放置在row行column列上，其格子裡填寫value資料
def returnStrDayList(startYear,startMonth,endYear,endMonth,day = "01"):
    result=[]
    if startYear == endYear:
        for month in range(startMonth,endMonth+1):
            month = str(month)
            if len(month) == 1:
                month = "0" + month
            result.append(str(startYear)+month+day)
        return result
    for year in range(startYear,endYear+1):
        if year == startYear:
            for month in range(startMonth,13):
                month = str(month)
                if len(month)==1:
                    month="0"+month
                result.append(str(year)+month+day)
        elif year == endYear:
            for month in range(1,endMonth+1):
                month = str(month)
                if len(month)==1:
                    month="0"+month
                result.append(str(year)+month+day)
        else:
            for month in range(1,13):
                month = str(month)
                if len(month)==1:
                         month="0"+month
                result.append(str(year)+month+day)
    return result        



# 讀取XML文件
tree=ET.parse("New.xml")
root = tree.getroot()
data_dict = xml_to_dict(root)
print(data_dict)

# # 將XML轉換為字典格式
# stock_data = {}
# for element in root.iter():
#     if element.text is not None:
#         stock_data[element.tag] = element.text

fields={"日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"}
wb=Workbook()#建立excel檔案
sheet=wb.active#讓excel啟動，建立第一個工作表格

sheet.title='fields'
# 將資料放置ˋ在row行column列上，其格子裡寫value資料
fillSheet(sheet,fields,1)#執行函式，注意參數要放對
startYear,startMonth=int(data_dict["startYear"]),int(data_dict["startMonth"])
endYear,endMonth=int(data_dict["endYear"]),int(data_dict["endMonth"])
yearList=returnStrDayList(startYear,startMonth,endYear,endMonth)
#print(yearList)
row = 2
for YearMonth in yearList:
    rq=requests.get(data_dict['url'],params={
        'response':"json",
        "date":YearMonth,
        "stockNo":data_dict['stockNo']
    })
    jsonData=rq.json()
    dailyPriceList=jsonData.get('data',[])
    for  dailyPrice in dailyPriceList :
        fillSheet(sheet,dailyPrice,row)
        row+=1                           
    time.sleep(3)
name= data_dict["excelName"]
wb.save(name+".xlsx") #save
