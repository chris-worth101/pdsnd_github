# Databricks notebook source
import time
import datetime
import pandas as pd
import numpy as np

#v1.0
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city = ''
month = ''
day = ''
sel_city = ''
sel_month = ''
sel_day = ''

def get_filters(city,month,day):
  """
  Asks user to specify a city, month, and day to analyze.
  Returns:
      (str) city - name of the city to analyze
      (str) month - name of the month to filter by, or "ALL" to apply no month filter
      (str) day - name of the day of week to filter by, or "ALL" to apply no day filter
      Although stored as a string, the user input is a number.
  """
  print('Hello! Let\'s explore some US bikeshare data!')
  #get city by capturing the number input by the user
  while True:
    print('Please select one of the Cities below by entering a number 1 - 3:\n1: Chicago\n2: New York City\n3: Washington')
    #get user input here
    city_num = input('Please enter a number 1 - 3:')
    
    #check user input is a number from 1 - 3
    if city_num not in['1','2','3']:
      print('Please Select a City by entering a number 1 - 3:')
    else:     
      break

  #set city name by checking the number input by the user
  if int(city_num) == 1:
    city = 'chicago'
  elif int(city_num) == 2:
    city = 'new york city'
  elif int(city_num) == 3:
    city = 'washington'
      
 #get month by capturing the number input by the user
  while True:
    print('Please Select a Month by entering a number 1 - 6:\n1 = January etc.\nEnter 0 to select ALL')
    #get user input here
    month_num = input()

    #check the number the user input
    if month_num not in['0','1','2','3','4','5','6']:
      print('Please Try Again')
    else:
      if month_num == '0':
        #set month to be ALL
        month = 'ALL'
      else:
        #convert the month_num to be the month name
        month = datetime.date(1900, int(month_num), 1).strftime('%B')
      break

  # get Day by capturing the number input by the user
  while True:
    print('Please Select a Day by entering a number 1 - 7:\n1 = Monday etc.\nEnter 0 to select ALL')
    #get user input
    day_num = input()

    #check user input is a number from 0 - 7
    if day_num not in['0','1','2','3','4','5','6','7']:
      print('Please Try Again')
    else:
      if day_num == '0':
        #set day to be ALL
        day = 'ALL'
      else:
        #convert day_num to the day name
        day = datetime.date(1900, 1, int(day_num)).strftime('%A')
      break 
  
  #return values here
  return city, month, day


def load_data(city, month, day):
  """
  Loads data for the specified city and filters by month and day if applicable.
  Args:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "ALL" to apply no month filter
    (str) day - name of the day of week to filter by, or "ALL" to apply no day filter
    Although stored as a string, the user input is a number.
  Returns:
    df - pandas DataFrame containing city data filtered by month and day
  """

  print('Loading Data, Please Stand By...')  
  # load data file into a dataframe
  df = pd.read_csv(CITY_DATA[city])

  # convert the Start Time column in the datetime to be dates/times
  df['Start Time'] = pd.to_datetime(df['Start Time']) 

  # extract month, weekday name and hour from Start Time to create new columns
  df['month'] = df['Start Time'].dt.month #make month number column
  df['Weekday Name'] = df['Start Time'].dt.strftime('%A') #make weekday name column
  df['hour'] = df['Start Time'].dt.hour # extract hour from the Start Time column

  # filter by month if not ALL
  if month != 'ALL':
    # use the index of the months list to get the corresponding int
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month = months.index(month)+1
    
    # filter by month to create the new dataframe
    df = (df.loc[df['month'] == month])

  # filter by day of week if not ALL
  if day != 'ALL':
    # filter by day of week to create the new dataframe
    df = (df.loc[df['Weekday Name'] == day])
  
  return df

def time_stats(df,sel_month,sel_day):
  """Displays statistics on the most frequent times of travel."""

  print('-'*40)
  print('\nCalculating The Most Frequent Times of Travel...\n')
  start_time = time.time()

  #get the most popular time stats
  popular_month = df['month'].mode()[0]
  popular_day = df['Weekday Name'].mode()[0]
  popular_hour = df['hour'].mode()[0]
  month_name = datetime.date(1900, popular_month, 1).strftime('%B') #convert the popular_month to be the month name

  # if sel_month or sel_day = ALL then display the most common month & day of week
  # else show selected_month & selected_day
  # always show Most Frequent Start Hour

  #print Stats
  print('1. Popular Times of Travel\n')
  if sel_month == 'ALL':
    print('The Most Frequent Month is:', month_name)
  else:
    print('You Selected the Month:', sel_month)
  if sel_day == 'ALL':
    print('The Most Frequent Day is:', popular_day)
  else:
    print('You Selected the Day:', sel_day)

  print('The Most Frequent Start Hour is:', popular_hour)
  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)


def station_stats(df):
  """Displays statistics on the most popular stations and trip."""

  print('\nCalculating The Most Popular Stations and Trip...\n')
  start_time = time.time()
    
  #first we make the Combined Start_End Station Column
  df['Start End'] = df['Start Station'] + ' to ' + df['End Station']
    
  #get the most commonly used
  Start_Station = df['Start Station'].mode()[0] #Start Station
  End_Station = df['End Station'].mode()[0] #End Station
  Start_End = df['Start End'].mode()[0] #Cobination of the two

  #get counts
  Start_Station_Count = sum(df['Start Station']== Start_Station)
  End_Station_Count = sum(df['End Station']== End_Station)
  Combo_Station_Count = sum(df['Start End']== Start_End)

  #print Stats
  message = '2. Popular Stations and Trips\n\nThe Most Commonly used Start Station is: {} with a count of: {}\nThe Most Commonly used End Station is: {} with a count of: {}\nThe Most Common Journey is: {} with a count of: {}'
  print(message.format(Start_Station,Start_Station_Count,End_Station,End_Station_Count,Start_End,Combo_Station_Count))

  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)


def trip_duration_stats(df):
  """Displays statistics on the total and average trip duration."""

  print('\nCalculating Trip Duration...\n')
  start_time = time.time()

  #get Travel Times
  Total_Travel = df['Trip Duration'].sum()
  Avg_Travel_Time = df['Trip Duration'].mean()
  Min_Time = df['Trip Duration'].min()
  Max_Time = df['Trip Duration'].max()

  #convert Total_Travel to Days, Hours, Minutes and Seconds
  total_days = Total_Travel // 86400
  Total_Travel = Total_Travel % 86400
  total_hrs = Total_Travel // 3600
  Total_Travel = Total_Travel % 3600
  total_mins = Total_Travel // 60
  total_sec = round(Total_Travel % 60,2)

  #convert Avg_Travel_Time to Days, Hours, Minutes and Seconds
  avg_days = Avg_Travel_Time // 86400
  Avg_Travel_Time = Avg_Travel_Time % 86400
  avg_hrs = Avg_Travel_Time // 3600
  Avg_Travel_Time = Avg_Travel_Time % 3600
  avg_mins = Avg_Travel_Time // 60
  avg_sec = round(Avg_Travel_Time % 60,2)

  #convert Min_Time to Days, Hours, Minutes and Seconds
  min_days = Min_Time // 86400
  Min_Time = Min_Time % 86400
  min_hrs = Min_Time // 3600
  Min_Time = Min_Time % 3600
  min_mins = Min_Time // 60
  min_sec = round(Min_Time % 60,2)
    
  #convert Max_Time to Days, Hours, Minutes and Seconds
  max_days = Max_Time // 86400
  Max_Time = Max_Time % 86400
  max_hrs = Max_Time // 3600
  Max_Time = Max_Time % 3600
  max_mins = Max_Time // 60
  max_sec = round(Max_Time % 60,2)

  #print Stats
  print('3. Trip Durations\n')
  message = 'The Total Travel Time is: {} Days, {} Hours, {} Minutes, {} Seconds'
  print(message.format(total_days,total_hrs,total_mins,total_sec))
  message = 'The Mean Average Time is: {} Days, {} Hours, {} Minutes, {} Seconds'
  print(message.format(avg_days,avg_hrs,avg_mins,avg_sec))
  message = 'The Minimum Time is: {} Days, {} Hours, {} Minutes, {} Seconds'
  print(message.format(min_days,min_hrs,min_mins,min_sec))
  message = 'The Maximum Time is: {} Days, {} Hours, {} Minutes, {} Seconds'
  print(message.format(max_days,max_hrs,max_mins,max_sec))

  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)


def user_stats(df,sel_city):
  """
  Displays statistics on bikeshare users.
  Including Gender and Year of Birth, if Found
  """

  print('\nCalculating User Stats...\n')
  start_time = time.time()

  #get users stats
  user_types_count = df['User Type'].value_counts()
  user_type = user_types_count.index  #get the user type descriptions
  user_count = user_types_count.values  #get the user type count values
  num1 = user_types_count.size  #get the row count of user types
  blank_num1 = df.shape[0] -(sum(user_types_count.values))  #get the count of blanks

  if sel_city != 'washington':
    #get the Gender stats
    gender_count = df['Gender'].value_counts()
    gen_type = gender_count.index #get the gender type descriptions
    gen_count = gender_count.values #get the gender type count values
    num2 = gender_count.size  #get the row count of gender types
    blank_num2 = df.shape[0] -(sum(gender_count.values))  #get the count of blanks

    #get year of birth stats
    min_birth_year = int(df['Birth Year'].min())
    max_birth_year = int(df['Birth Year'].max())
    mode_birth_year = int(df['Birth Year'].mode()[0])

  #print Stats
  print('4. The Following User Types Were Found:\n')
  #cycle thourgh each row of user type found, and output results. Output the count of any Blanks found
  for n in range(num1):
    print (user_type[n],':', user_count[n])
  print('There were {} blanks found.\n'.format(blank_num1))

  if sel_city != 'washington':
    #cycle thourgh each row of Gender type found, and output results
    for n in range(num2):
      print (gen_type[n],':', gen_count[n])
      
    #output the count of any Blanks found and the Year of Birth stats
    message = 'There were {} blanks found.\n\nThe Earliest Year of Birth is: {}\nThe Latest Year of Birth is: {}\nThe Most Common Year of Birth is: {}'
    print(message.format(blank_num2,min_birth_year,max_birth_year,mode_birth_year))

  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)

def see_data(df):
  ''' 
  Asks the user if they would like to see the first 5 rows of data.
  If they say yes it will then ask if they would like to see the next 5 rows of data.
  It will keep doing this until the user says no.
  '''
  #ensure we can see all the columns of data!
  pd.set_option("display.max_columns", 200)

  #set start row and see_first flag to true
  start_row = 0
  see_first = True
  while (see_first):
    #get user input
    see_first = input('Would you like to see the first 5 rows of data? Enter yes or no.')
    start_time = time.time()
    if see_first.lower() != 'yes':
      break
    #print first 5 rows of data
    print('\nGetting Data...\n')
    #ensure we can see all the columns of data!
    pd.set_option("display.max_columns", 200)
    print(df.head())
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    #ask user if they would like to see the next 5 rows
    while True:
      #get user input
      see_next = input('whould you like to see the next 5 rows of data? Enter yes or no.')
      start_time = time.time()
      if see_next.lower() !='yes':
        #set the see_first flag to false
        see_first = False
        break

      #add 5 to the start row and get next 5 rows of data
      start_row += 5
      print('\nGetting Data...\n')
      #ensure we can see all the columns of data!
      pd.set_option("display.max_columns", 200)
      print(df.iloc[start_row:start_row + 5])
      print("\nThis took %s seconds." % (time.time() - start_time))

def main1():
  #run all Functions
  while True:
    #get filters
    filter = True
    while (filter):
      sel_city, sel_month, sel_day = get_filters(city, month, day)
      print('-'*40)
      message = 'You have selected the following:\nThe City of: {}\nThe Month of: {}\nThe Day: {}'
      print(message.format(sel_city.title(),sel_month,sel_day))
      filter = input('Is this correct? Enter yes or no.')
      if filter.lower() == 'yes':
        break

    #get data frame
    df = load_data(sel_city, sel_month, sel_day)
    
    #get Time stats
    time_stats(df,sel_month,sel_day)

    #get Station Stats
    station_stats(df)

    #get duration stats
    trip_duration_stats(df)

    #get user stats
    user_stats(df,sel_city)

    print('-'*40)
    print('this gives us a row count of: ', df.shape[0])

    #view data?
    see_data(df)
    
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes':
      break


#if __name__ == "__main__":
#  main1()
  



# COMMAND ----------

main1()
