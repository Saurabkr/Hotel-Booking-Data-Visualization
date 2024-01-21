import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np
warnings.filterwarnings('ignore')

df = pd.read_csv("hotel_bookings.csv")
print(df.head(10))
print(df.shape) #To find the number of column and row in csv file
print(df.columns)

#To check the data type of each column
print(df.info())

#To change the data type of required column
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'],format='%d/%m/%Y')
print(df.info())
print(df.describe(include='object'))

#To get the column name which has object as data type, also find the unique value of column
for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print(50*'-')

#To get the count of column which have NULL value in it.
print(df.isnull().sum())

#Drop the column which have NULL value
df.drop(['agent','company'], axis=1, inplace=True)
df.dropna(inplace=True) #It will drop all NULL value in the table i.e babies and country
print(df.isnull().sum())

#we can identify and remove the outliers
print(df.describe())#use to give info about column whose data type is not object
# df['adr'].plot(kind='box') #Get the graph of outliers if any

df = df[df['adr']<5000] #Remove outlier if any

#now we start visualization of data
#Visualizing the count of cancelled and non cancelled reservation using matplotlib
percentage_cancl = df['is_canceled'].value_counts(normalize=True)
print(percentage_cancl)

plt.figure(figsize=(5,5))
plt.title('Revervation Cancelled Count')

x = np.array(["Cancelled", "Not Cancelled"])
plt.xlabel("Hotel Reservation Status") 
y = df['is_canceled'].value_counts()
plt.ylabel("Count")

plt.bar(x,y, edgecolor='k', width=0.3)

for i ,txt in enumerate(y):
    plt.text(i, txt, str(txt), ha='center', va='bottom')

plt.show()    

#Visualizing the count of resevtion cancelled/not cancelled in resort or city hotels using seaborn

plt.figure(figsize=(8,5))
plt.title('Reservation Status in different hotels', size=(15))
plt.xlabel('Hotels-->')
plt.ylabel('No. of Reservations-->')

plot = sns.countplot(x='hotel', hue='is_canceled', data=df, palette='Blues')
plot.get_legend_handles_labels()
plot.legend(bbox_to_anchor=(1,1))
plt.show()

#Visualization of average daily rate(adr) of resort and city hotel
resort_hotels = df[df['hotel']=='Resort Hotel']
resortHotels_per=resort_hotels['is_canceled'].value_counts(normalize=True)
print(resortHotels_per)

city_hotels = df[df['hotel']=='City Hotel']
cityHotels_per=city_hotels['is_canceled'].value_counts(normalize=True)
print(cityHotels_per) #city Hotels cancelation rate is higher

resort_hotels = resort_hotels.groupby('reservation_status_date')[['adr']].mean()
city_hotels = city_hotels.groupby('reservation_status_date')[['adr']].mean()

plt.figure(figsize=(20,10))
plt.title('Average daily rate in City and Resort Hotel', fontsize=20)
plt.plot(resort_hotels.index, resort_hotels['adr'], label='Resort Hotel')
plt.plot(city_hotels.index, city_hotels['adr'], label='City Hotel')
plt.legend(fontsize=20)
plt.show()

#Visalization of month in which max. cancelation happened
df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize=(15,8))
plt.title('Reservation Status in different hotels', size=(15))
plt.xlabel('Hotels-->')
plt.ylabel('No. of Reservations-->')

plot = sns.countplot(x='month', hue='is_canceled', data=df, palette='bright')
plot.get_legend_handles_labels()
plot.legend(['Non Canceled','Canceled'])
plt.show()

#Visualization of adr when reservation was canceled
plt.figure(figsize=(15,8))
plt.title('adr per month', fontsize=20)
sns.barplot(x='month', y='adr', data = df[df['is_canceled']==1].groupby('month')[['adr']].sum().reset_index())
plt.show() #From this plot we can conclude the price high can be the one factor for cancelation

#Visualiztion of countries that have high cancelation
canceled_data = df[df['is_canceled']==1]
top_ten = canceled_data['country'].value_counts()[:10]
plt.figure(figsize=(8,8))
plt.title("Top 10 countries with maximum Cancelation")
plt.pie(top_ten, autopct='%.2f', labels= top_ten.index)
plt.show()

#findings: which market segmnet has the maximum cancelation
df['market_segment'].value_counts(normalize=True)
canceled_data['market_segment'].value_counts(normalize=True)

#Visualization of adr for canceled or non canceled resevation
canceled_data = df[df['is_canceled']==1]
canceled_df_adr = canceled_data.groupby('reservation_status_date')[['adr']].mean().reset_index()
canceled_df_adr.sort_values('reservation_status_date', inplace=True)

notcanceled_data = df[df['is_canceled']==0]
notcanceled_df_adr = notcanceled_data.groupby('reservation_status_date')[['adr']].mean().reset_index()
notcanceled_df_adr.sort_values('reservation_status_date', inplace=True)

# canceled_df_adr['reservation_status_date'] = pd.to_datetime('reservation_status_date')
# notcanceled_df_adr['reservation_status_date'] = pd.to_datetime('reservation_status_date')

canceled_df_adr = canceled_df_adr[(canceled_df_adr['reservation_status_date']>'2016') & (canceled_df_adr['reservation_status_date']<'2017-09')]
notcanceled_df_adr = notcanceled_df_adr[(notcanceled_df_adr['reservation_status_date']>'2016') & (notcanceled_df_adr['reservation_status_date']<'2017-09')]

plt.figure(figsize=(20,6))
plt.title("Average daily rate")
plt.plot(canceled_df_adr['reservation_status_date'], canceled_df_adr['adr'], label='Canceled')
plt.plot(notcanceled_df_adr['reservation_status_date'], notcanceled_df_adr['adr'], label='Not Canceled')
plt.legend()
plt.show()


