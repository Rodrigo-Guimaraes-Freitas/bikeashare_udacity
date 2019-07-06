#!/usr/bin/env python
# coding: utf-8

# In[22]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
city_verification = ["Chicago", "New York", "Washington"]
month_verification = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
day_verification = ['Monday', 'Tuesday','Wednesday', ' Thursday', 'Friday', 'All']
Binary_condition = ['Yes', 'No']


# In[25]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city.title()])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
    df['End Time'] = pd.to_datetime(df['End Time']) 
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour']=df['Start Time'].dt.hour
    df['end_hour']=df['End Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1

    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    raw_data_displayer = input('Would you like to see a preview ofd the raw data generated? ')
    raw_data_displayer=raw_data_displayer.title()
    if raw_data_displayer == "Yes":
        while raw_data_displayer == "Yes":
            n = input("How many lines would you like to see?")
            print(n.isnumeric())
            while n.isnumeric() == False:
                n = input("Please insert a valid integer number!")
            n = float(n)
            while int(n) > df.shape[0]:
                n = input("Please insert a valid number of lines. The database has {} lines".format(df.shape[0]))    
            print(df.head(int(n)))
            raw_data_displayer = input('Would you like to check it again? ')
            raw_data_displayer = raw_data_displayer.title()
            while raw_data_displayer not in Binary_condition:
                raw_data_displayer = input('Please answer Yes or No to this question. Would you like to check it again? ')
                    
    return df


# In[26]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you like to analyze? Choose Chicago, New York or Washington: ")
    city = city.title()
    while city not in city_verification:
        city = input("Please insert a valid city. We have data available for the cities Chicago, New York and Washington ")
        city = city.title()
    # get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to analyze? january, february, march, may, june or all? ")
    month=month.title()
    while month not in month_verification:
        month = input("Please insert a valid month. We have data available from January to June ")
        month=month.title()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    day = input("Now choose the day of week. monday, tuesday, wednesday, thursday, friday or all. ")
    day = day.title()
    while day not in day_verification:
        day = input("Please choose a valid day of week. monday, tuesday, wednesday, thursday, friday or all. ")
        day = day.title()
    
    print('-'*80)
    return city, month, day


# In[27]:


def time_stats(day,month,df):

    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
 
    
    if str(month) == 'All':
        # display the most common month
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        popular_month = df['month'].mode()
        print('Most Frequent month:', months[popular_month[0]-1].title())
    if str(day) == 'All':
        # display the most common day of week
        popular_dow = df['day_of_week'].mode()
        print('Most Frequent day of the week:', popular_dow.to_string(index=False))
    # display the most common start hour
    popular_start_hour = df['start_hour'].mode()
    print('Most Frequent Start Hour:', popular_start_hour.to_string(index=False))
    popular_end_hour = df['end_hour'].mode()
    print('Most Frequent End Hour:', popular_end_hour.to_string(index=False))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


# In[28]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()
    print('Most Frequent Start Station:', popular_start_station.to_string(index=False))
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()
    print('Most Frequent End Station:', popular_end_station.to_string(index=False))
    
    # display most frequent combination of start station and end station trip
    #popular_combination = df["station_combination"].mode()
    #print('Most Frequent combination:', popular_combination.to_string(index=False))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[35]:



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/3600
    print('Total time traveled in hours:', total_travel_time.astype(float).round(decimals=2).tolist())
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('Mean Trip duration in minutes:', mean_travel_time.astype(float).round(decimals=2).tolist())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[36]:


def user_stats(city,df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df.groupby('User Type').size()
    user_types_count.tolist()
    print('Quantity of users by type:')
    print(user_types_count)
    
    # Display counts of gender
    if city == "Washington":
        print("Too bad! We do not have any information about genders and birth years to this city :( But I promisse you we will work on it!")
    
    else:
        user_genders_count = df.groupby('Gender').size()
        print('Quantity of users by gender:')
        print(user_genders_count)

    # Display most recent, and most common year of birth
    if city != "Washington":
        Most_common_YOB=df['Birth Year'].mode()
        youngest_year = df['Birth Year'].max()
        oldest_year = df['Birth Year'].min()

        print('Most common birth year', Most_common_YOB.tolist())
        print('Birth year of the youngest users', youngest_year)
        print('Borth year of the oldest users', oldest_year)
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# def main():
#     while True:
#         city, month, day = get_filters()
#         df = load_data(city, month, day)
#         time_stats(day,month,df)
#         station_stats(df)
#         trip_duration_stats(df)
#         user_stats(df)
#      
#         restart = input('\nWould you like to restart? Enter yes or no.\n')
#         if restart.lower() != 'yes':
#             print("Thank you for your time! See you soon <3")
#             break
#         else:
#             print("Uhuu here we go again!")
# 
# if __name__ == "__main__":
# 	main()
# 

# In[37]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(day,month,df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city,df)
     
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for your time! See you soon <3")
            break
        else:
            print("Uhuu here we go again!")

if __name__ == "__main__":
	main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




