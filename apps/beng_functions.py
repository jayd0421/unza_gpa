import streamlit as st

def departments_list(data):
    """Returns a list of all the departments in the dataframe

    Args:
        data (dataframe): dataframe with columns 'program_id' and 'program'

    Returns:
        type: list
    """

    # Get dictionary of all programs
    programs_dict = dict(zip(data['program_id'], data['program']))

    # Get dictionary of beng departments
    programs_dict = dict(sorted(programs_dict.items())[:5])

    # Get list of beng departments
    departments_list = list(programs_dict.values())

    return departments_list

def years_of_study_list(data):
    """Returns a list of all the years of study in the dataframe

    Args:
        data (dataframe): dataframe with columns 'year_id' and 'year'

    Returns:
        type: list
    """

    # Get dictionary of all programs
    years_of_study_dict = dict(zip(data['year_id'], data['year']))

    # Get dictionary of beng departments
    years_of_study_dict = dict(sorted(years_of_study_dict.items()))

    # Get list of beng departments
    years_of_study_list = list(years_of_study_dict.values())

    return years_of_study_list

def department_df(data, department, year):
    # Get first or second year courses
    if year == "First" or year == "Second":
        departments_df = data[(data['year'] == year)]
    # Get specialised courses
    else:
        departments_df = data[(data['program'] == department)  & (data['year'] == year)]
    
    return departments_df