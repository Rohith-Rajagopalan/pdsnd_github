import time
import pandas as pd
import numpy as np
from tabulate import tabulate


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = input('Enter city:').lower()
    while city not in ('chicago','washington','new york city'):
        print('Incorrect city name. Please choose from chicago, new york city, and washington')
        city = input('Enter city:').lower()
    # get user input for month (all, january, february, ... , june)
    month = input('Enter month:').lower()
    while month not in ('january', 'february', 'march', 'april', 'may', 'june','all'):
        print('Incorrect month. Please choose from the first six months of the year or enter "all"')
        month = input('Enter month:').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter day:').lower()
    while day not in ('saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday','friday','all'):
        print('Incorrect entry. Please enter again or enter "all"')
        day = input('Enter day:').lower()


    print('-'*40)
    return city, month, day


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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
     # filter by month

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    print('Most common month:', df['Start Time'].dt.month_name().mode())

    # display the most common day of week
    print('Most common day:', df['Start Time'].dt.weekday_name.mode())

    # display the most common start hour
    print('Most common hour:', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station:',df['Start Station'].mode().values[0])

    # display most commonly used end station
    print('Most commonly used end station:',df['End Station'].mode().values[0])

    # display most frequent combination of start station and end station trip
    df['Station combination'] = df['Start Station']+' and '+df['End Station']
    print('Most commonly used station combination:',df['Station combination'].mode().values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['End Time'] = df['End Time'].astype('datetime64')
    order=input('Would you like to see the times in chronological or reverse chronological order(enter c/r):')
    num=int(input('How many rows would you like to see (enter number):'))

    # display total travel time
    df = df.sort_values(by=['Start Time'])
    df['Trip Duration (in minutes)'] = round(df['Trip Duration']/60,2)
    x=num

    if order!= 'r':
        print(df[['Start Time','End Time','Trip Duration (in minutes)']].head(num))
        request=input('Would you like to see the next {} rows (yes/no):'.format(num)).lower()
        while request != 'no':
           print(df[['Start Time','End Time','Trip Duration (in minutes)']][x:x+num])
           request=input('Would you like to see the next {} rows (yes/no):'.format(num)).lower()
           x+=num
    else:
        print(df[['Start Time','End Time','Trip Duration (in minutes)']].tail(num))
        request=input('Would you like to see the next {} rows (yes/no):'.format(num)).lower()
        reversed_df = df.iloc[::-1]
        while request != 'no':
           print(reversed_df[['Start Time','End Time','Trip Duration (in minutes)']][x:x+num])
           request=input('Would you like to see the next {} rows (yes/no):'.format(num)).lower()
           x+=num

    # display mean travel time
    print('\nMean travel time of all trips taken:', round(df['Trip Duration'].mean()/60,2), ' minutes')

    # calculating maximum and minimum travel time
    maxtime = df['Trip Duration'].max()
    start_st_max = df.loc[df['Trip Duration'] == maxtime, 'Start Station'].values[0]
    end_st_max = df.loc[df['Trip Duration'] == maxtime, 'End Station'].values[0]
    mintime=df['Trip Duration'].min()
    start_st_min = df.loc[df['Trip Duration'] == mintime, 'Start Station'].values[0]
    end_st_min = df.loc[df['Trip Duration'] == mintime, 'End Station'].values[0]

    # display maximum travel time
    print('\nLongest trip ever taken was from {} to {} and lasted {} minutes'.format(start_st_max,end_st_max,round(maxtime/60,2)))
    print('\nStart time for longest trip=',df.loc[df['Trip Duration'] == maxtime, 'Start Time'].values[0])
    print('\nEnd time for longest trip=',df.loc[df['Trip Duration'] == maxtime, 'End Time'].values[0])

    # display minimum travel time
    print('\nShortest trip ever taken was from {} to {} and lasted {} minutes'.format(start_st_min,end_st_min,round(mintime/60,2)))
    print('\nStart time for shortest trip=',df.loc[df['Trip Duration'] == mintime, 'Start Time'].values[0])
    print('\nEnd time for shortest trip=',df.loc[df['Trip Duration'] == mintime, 'End Time'].values[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user types:\n', df['User Type'].value_counts())

    #check if gender column exists (.i.e. if city is NYC or chicago)
    if 'Gender' in df:
        # Display counts of gender
        genderrequest= input('Would you like to see gender count (yes/no)?:').lower()
        if genderrequest != 'no':
            print('\nCount by gender:\n', df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        birthrequest= input('Would you like to see birth year statistics (yes/no)?:').lower()
        if birthrequest != 'no':
            print('\nEarliest Year of Birth:', df['Birth Year'].min())
            print('\nLatest Year of Birth:', df['Birth Year'].max())
            print('\nMost common Year of Birth:', df['Birth Year'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def raw_data(df):
    """Displays statistics on the total and average trip duration."""

    start_time = time.time()
    df['End Time'] = df['End Time'].astype('datetime64')
    answer = input('Would you like to see the first 5 rows of the complete trip data (yes/no):').lower()
    if answer != 'no':
        order=input('Would you like to see the times in chronological or reverse chronological order(enter c/r):')
        df = df.sort_values(by=['Start Time'])
        df['Trip Duration (in minutes)'] = round(df['Trip Duration']/60,2)
        x=5
        
        if order!= 'r':
            print(tabulate(df.head(5), headers ="keys"))
            request=input('Would you like to see the next 5 rows (yes/no):').lower()
            while request != 'no':
                print(tabulate(df.iloc[np.arange(x,x+5)], headers ="keys"))
                request=input('Would you like to see the next 5 rows (yes/no):').lower()
                x+=5
        else:
            print(df.tail(5))
            request=input('Would you like to see the next 5 rows (yes/no):').lower()
            reversed_df = df.iloc[::-1]
            while request != 'no':
                print(reversed_df.iloc[x:x+5])
                request=input('Would you like to see the next 5 rows (yes/no):').lower()
                x+=5


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
