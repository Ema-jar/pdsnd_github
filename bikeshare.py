import time
import datetime
from random import randrange
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

SELECTABLE_CITIES = tuple(CITY_DATA)
SELECTABLE_MONTHS = tuple(["all", "january", "february", "march", "april", "may", "june", "july", "august","september", "october", "november", "dicember"])
SELECTABLE_DAYS = tuple(["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
SELECTABLE_N_ROWS = tuple(["random", "10", "30", "42", "50", "quit"])

def init_df(df):
    """
    Initialize the data frame for the next computations
    
    1) convert Start Time column to datetime
    2) convert End Time column to datetime
    3) add a month column created from Start Time and containing the name of the month (e.g. January, February,...)
    4) add a day column created from Start Time and containing the name of the day (e.g. Monday, Tuesday,...)
    5) add a hour column created from Start Time and containing the hour in 24-hour clock format (e.g. 9, 13, 22...)
    """
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Specify the name of the city according to this format {}'.format(SELECTABLE_CITIES))
    city = collect_user_input(SELECTABLE_CITIES)

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Specify the name of the month according to this format {}, use "all" if you want to consider all of them'.format(SELECTABLE_MONTHS))
    month = collect_user_input(SELECTABLE_MONTHS)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Specify the name of the day according to this format {}, use "all" if you want to consider all of them'.format(SELECTABLE_DAYS))
    day = collect_user_input(SELECTABLE_DAYS)

    print('-'*40)
    return city, month, day

def collect_user_input(available_options):
    """
    Collect a user input and match this input against a list of available options. The process continues
    until the user inserts a valid input.
    
    Returns:
        (str) an input contained in the available_options tuple
    """
   
    option = ''
    while option == '':
        option = input().lower()
        if option not in available_options:
            print('Option {} is not available. Avaialable options are {} - try again!'.format(option, available_options))
            option = ''

    return option

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

    # initialize the data frame
    init_df(df)
    
    size_before = len(df.index)
    print('{} rows BEFORE filter application'.format(size_before))

    # filter rows
    if month != 'all':
        df = df.loc[df['month'] == month.title()]

    if day != 'all':
        df = df.loc[df['day'] == day.title()]
        
    size_after = len(df.index)
    print('{} rows AFTER filter application'.format(size_after))

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month, number_trips_month = calculate_max_frequency(df, 'month')
    print('{} travels have been started on {}'.format(number_trips_month, most_common_month))

    # TO DO: display the most common day of week
    most_common_day, number_trips_day = calculate_max_frequency(df, 'day')
    print('{} travels have been started on {}'.format(number_trips_day, most_common_day))

    # TO DO: display the most common start hour
    most_common_hour_start, number_trips_hour = calculate_max_frequency(df, 'hour')
    most_common_hour_end = (most_common_hour_start + 1) % 24
    print('{} travels have been started between {}:00 and {}:00'
          .format(number_trips_hour, most_common_hour_start, most_common_hour_end)
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_st_name, start_st_frequency = calculate_max_frequency(df, 'Start Station')
    print('The most common used started station is {} used {} times'.format(start_st_name, start_st_frequency))
    
    # TO DO: display most commonly used end station
    end_st_name, end_st_frequency = calculate_max_frequency(df, 'End Station')
    print('The most common used end station is {} used {} times'.format(end_st_name, end_st_frequency))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start to End'] = df['Start Station'] + '>' + df['End Station']    
    se_st_name, se_st_frequency = calculate_max_frequency(df, 'Start to End')
    splitted_stations = se_st_name.split('>')
    print('People have moved from {} to {}, {} times.'
          .format(splitted_stations[0], splitted_stations[1], se_st_frequency)
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def calculate_max_frequency(df, column_name):
    """
    Calculates the max frequency of a value in a column specified by column_name
    
    Returns:
        (str) first_value: the name of the value
        (int) first_frequency: the frequency of this falue in the column
    """

    if len(df.index) == 0:
        raise ValueError("DataFrame cannot be empty")

    values_counted = df[column_name].value_counts(sort=True, dropna=True)
    first_value = values_counted.index[0]
    first_frequency = values_counted[first_value]
    
    return first_value, first_frequency

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TODO: extract trip duration if not present
    if not duration_info_are_present(df):
        print('WARNING - Statistics about trip duration cannot be calculated because Trip Duration data are missing and this information cannot be retrieved using other columns')
    
    seconds_in_hour = 3600
    seconds_in_min = 60

    # TO DO: display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    tot_to_hours = tot_travel_time // seconds_in_hour
    print('The total amount of time spent traveling is {} seconds (c.{} hours)'.format(tot_travel_time, tot_to_hours))

    # TO DO: display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    avg_to_min = avg_travel_time // seconds_in_min
    print('The mean amount of time spent traveling is {} seconds (c.{} minutes)'.format(avg_travel_time, avg_to_min))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def duration_info_are_present(df):
    """
        Check if the "Trip Duration" column is present in the data frame and tries to
        infer this information using "Start Date" and "End Date" columns.

        Returns:
            (bool) true - if the "Trip Duration" is in the df
            (bool) false - if the "Trip Duration" is not in the df and it's not possible
            to infer this information
    """
    
    if('Trip Duration' not in df.columns):
        if not ('Start Time' in df.columns and 'End Time' in df.columns):
            return False
        else:
            df['Trip Duration'] = df['End Time'] - df['Start Time']
    
    return True
        

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts(dropna=True)
    print('Users are divided into {} categories:'.format(len(user_types.index)))
    for entry in user_types.index:
        print(' - {}: {}'.format(entry, user_types[entry]))
    
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts(dropna=True)
        print('Users identify as:')
        for entry in genders.index:
            print(' - {}: {}'.format(entry, genders[entry]))
    else:
        print('WARNING - No information available for the user\'s gender')
    
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        older_user_yob = int(df['Birth Year'].min())
        older_age = int(datetime.datetime.now().year - older_user_yob)
        print('The oldest user is {} and was born in {} (earliest yob)'.format(older_age, older_user_yob))

        younger_user_yob = int(df['Birth Year'].max())
        younger_age = int(datetime.datetime.now().year - younger_user_yob)
        print('The younger user is {} and was born in {} (most recent yob)'.format(younger_age, younger_user_yob))

        common_yob, yob_frequency = calculate_max_frequency(df, 'Birth Year')
        print('{} users were born in {}, this is the most common year of birth'.format(yob_frequency, int(common_yob)))
    else:
        print('WARNING - No information available for the user\'s age and year of birth')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_rows(df, number_of_rows):
    """
    Display a number of rows of the data frame based on the passed value of number_of_rows
    """

    # print the first number_of_rows of the data frame 
    if number_of_rows not in ['random', '42', 'quit']:
        print(df[:int(number_of_rows)])
    # print an Ester Egg message
    elif number_of_rows == '42':
        print('Sorry but 42 is supposed to be The Answer, not a question, don\'t panic and try again :)')
    # print a random number (between 1 and 20) of rows from the data frame
    else:
        sample_value = randrange(1, 21)
        print(df.sample(n = sample_value))


def main():
    while True:
        city, month, day = get_filters()
        
        print('The following filter is being applied: \n -city: {} \n -month: {} \n -day: {}'.format(city, month, day))

        df = load_data(city, month, day)

        if len(df.index) != 0:
            # calculate and print all the stats
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            # after stats have been printed the user can see a sample of the data frame
            print('Would you like to see a sample of the users? Enter yes or no.')
            show_sample = collect_user_input(tuple(["yes", "no"]))
            while show_sample != 'no':
                print('How many rows do you want to see? Please respect this format {}, use "random" if you want to see a list of random rows or "quit" if you have seen enough rows for today'.format(SELECTABLE_N_ROWS))
                number_of_rows = collect_user_input(SELECTABLE_N_ROWS)
                if number_of_rows == 'quit':
                    show_sample = 'no'
                else:
                    print_rows(df, number_of_rows)

        else:
            print("No data left after filter application, please try again changing your filter")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
