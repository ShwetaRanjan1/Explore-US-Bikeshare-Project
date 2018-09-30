import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago' : 'chicago.csv',
              'new york city' : 'new_york_city.csv',
              'washington' : 'washington.csv' }
def get_filters():
    """
    Asks the user to specify a city,month, and day to analyze the data.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,or "all" to apply no specific month filter
        (str) day - name of the day of the week to filter by,or "all" to apply no specific day filter
    """
    how_many_hello = 1
    hello_string = """
    *     *  ******  *       *         ***     |
    *     *  *       *       *       *     *   |
    *******  ******  *       *       *     *   |
    *     *  *       *       *       *     *   |
    *     *  ******  ******  ******    ***     * """
    print(hello_string * how_many_hello)
    print('Join me! Let\'s explore some US bikeshare data!\n')
    # make list of city,month,day to test.
    city_list = ['chicago','new york city','washington']
    month_list = ['all','january','february','march','april','may','june']
    day_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    # get user input for city name (chicago,new york city,washington)
    city = input('--->You would like to explore the data for chicago,new york city or washington?\nPlease enter any of the above city names.\n')
    #using while loop to handle invalid input
    while city.lower() not in city_list:
        print('Sorry!That was an Invalid Input.')
        city = input('->Please enter chicago,new york city or washington to view it\'s data.\n')
    #get user input for month (january,february,march,april,may,june,all)
    month = input('\n--->You would like to filter the data by which month? january, february, march, april, may or june.\nEnter "all" to filter the data by all the months.\n')
    while month.lower() not in month_list:
        print('-->Oops!Invalid month entered.\nPlease enter a valid month.\n')
        month = input('->Enter any month from january to june or type "all" for all months filter\n')
    #get user input for day of week(monday,tuesday,wednesday,thursday,friday,saturday,sunday,all)
    day = input('\n--->You would like to view the data for which day of week ? monday, tuesday, wednesday, thursday, friday, saturday or sunday\nEnter "all" to view the data for the whole week.\n')
    while day.lower() not in day_list:
        print('-->It seems like you have entered a wrong day name.\n')
        day = input('Please re-enter the day name or type "all" to explore the data for whole week.\n')
    print('~'*40)
    return city.lower(),month.lower(),day.lower()
    
    
def load_data(city,month,day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze the data
        (str) month - name of the month to filter by, or "all" to apply no specific month filter
        (str) day - name of the day of week to filter by, or "all" to apply no specific day filter
    Returns:
        df - Pandas DataFrame containing city data which is filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']= df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
    if month !='all':
        months=['january','february','march','april','may','june']
        month = months.index(month) +1
        df = df[df['month']==month]
    if day !='all':
        df = df[df['day_of_week']==day.title()]
    return df
                
           
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
                
    print('\nCalculating the statistics of the Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    #display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    print("The Most Common Month where Bikeshare is in high demand is:",most_common_month)
                
    #display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    most_common_day = df['day_of_week'].mode()[0]
    print("The Bikes are shared most commonly on: ",most_common_day)
                
    #display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    most_common_start_hour=df['hour'].mode()[0]
    print("The Most Common Start Hour of the trip is :",most_common_start_hour) 
                
    print("\nThis computation took %s seconds." % (time.time() - start_time))
    print('~'*40)
                
                
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip ...\n')                
    start_time = time.time()
                
    #display most commonly used start station
    common_start_station =df['Start Station'].mode()[0]
    print("The most commonly used Start Station while begining the trip is :",common_start_station)
                
    #display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used End Station while ending the trip is :",common_end_station)
                
    #display most frequent combination of start station and end station trip
    df['combination']=df['Start Station'] + '---' + df['End Station']
    most_frequent=df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).idxmax(axis=1)
    print("The most frequent combination of start station and end station trip is: ",most_frequent)
    
    print("\nThis computation took %s seconds."% (time.time() - start_time))
    print('~'*40)
                
                
def trip_duration_stats(df):
    """Displays the statistics on the total and average trip duration."""
                
    print('\nCalculating Trip Duration Statistics ...\n')
    start_time = time.time()
    
    #display total time of travel
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    print("The total time of travel is:",(df['End Time']-df['Start Time']).sum())
    #display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean of the trip duration in seconds is:",mean_travel_time)
                
                
def user_stats(df):
    """It displays the statistics on bikeshare users."""
    
    print('\n Calculating User Statistics ...\n')
    start_time = time.time()
                
    # Display counts of user types
    types_of_users = df['User Type'].value_counts()
    print(types_of_users)
                
    # Display counts of gender
    try:
        types_of_gender = df['Gender'].value_counts()
        print(types_of_gender)
    except KeyError:
        print('--> Gender Types and Birth years cannot be computed as this dataframe does not have a Gender column')
              
    # Display earliest,most recent ,and most common year of birth
    try:
        df.sort_values(by=['Birth Year'],ascending=True)
        print("The Bike Share Data has the record of earliest year of birth as --> ",int(df["Birth Year"].min()))
        print("The Bike Share Data has the record of most recent year of birth as --> ",int(df["Birth Year"].max()))
        common_year_of_birth=int(df['Birth Year'].mode()[0])
        print("Majority of people using bike share system have a common birth year of --> ",common_year_of_birth)
    except:
        print("and a Birth Year column")
              
    print("\nThis computation took %s seconds." % (time.time() - start_time))
    print('~'*40)
              
              
def main():
   while True:
       city,month,day = get_filters()
       df =load_data(city,month,day)
              
       time_stats(df)
       station_stats(df)
       trip_duration_stats(df)
       user_stats(df)
              
       restart = input('\nWould you like to restart? Enter yes or no.\n')
       if restart.lower() !='yes':
           break
              
              
if __name__ == "__main__":
    main()              
              
              
    