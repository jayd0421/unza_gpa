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

def courses_dict(selected_department, department_df, electrical_specialty):
    # Get df for specific EEE specialization
    if selected_department == 'Electrical & Electronics':
        eletrical_specialties_dict = {
            "Electrical Machines and Power": 'ET', 
            "Electronics and Telecommunication": "EMP"}

        # Get filter our df for specific EEE specialization
        department_df = department_df[
            department_df['comment'] != eletrical_specialties_dict[electrical_specialty]
            ]

        # Get dictionary for compulsory courses
        compulsory_courses_dict = dict(zip(
            department_df[department_df['is_compulsory'] == 1]['course_code'], # course_code as key
            department_df[department_df['is_compulsory'] == 1]['course'] # course as value
            ))

        # Get dictionary for elective courses
        elective_courses_dict = dict(zip(
            department_df[department_df['is_compulsory'] == 0]['course_code'], # course_code as key
            department_df[department_df['is_compulsory'] == 0]['course'] #course as value
            ))

    # Get other departments
    else:
        # Get dictionary for compulsory courses
        compulsory_courses_dict = dict(zip(
            department_df[department_df['is_compulsory'] == 1]['course_code'],
            department_df[department_df['is_compulsory'] == 1]['course']
            ))

        # Get dictionary for elective courses
        elective_courses_dict = dict(zip(
            department_df[department_df['is_compulsory'] == 0]['course_code'],
            department_df[department_df['is_compulsory'] == 0]['course']
            ))

    return compulsory_courses_dict, elective_courses_dict

def course_credits_dict(selected_department, department_df, electrical_specialty):
    # Get df for specific EEE specialization
    if selected_department == 'Electrical & Electronics':
        eletrical_specialties_dict = {
            "Electrical Machines and Power": 'ET', 
            "Electronics and Telecommunication": "EMP"}

        # Get filter our df for specific EEE specialization
        department_df = department_df[
            department_df['comment'] != eletrical_specialties_dict[electrical_specialty]
            ]

        # Get dictionary for course credits
        course_credits_dict = dict(zip(
            department_df['course_code'], # course_code as key
            department_df['course_credit'] # course_credit as value
            ))

    # Get other departments
    else:
        # Get dictionary for compulsory courses
        course_credits_dict = dict(zip(
            department_df['course_code'], # course_code as key
            department_df['course_credit'] # course_credit as value
            ))

    return course_credits_dict

def year_gpa(year_grades_dict, course_credits_dict, year):
    # Grade and corresponding gpv
    grade_gpv_dict = {
        'A+': 5, 'A': 4, 'B+': 3.5, 'B': 3, 'C+': 2.37,
        'C': 1, 'D+': 0, 'D': 0, 'P': 0, 'S': 0}

    total_credits = []
    cc_gpvs = []
    for (course, grade) in year_grades_dict[year].items():
        if grade is None:
            pass
        else:
            grade_gpv = grade_gpv_dict[grade]
            course_credit = course_credits_dict[course]
            cc_gpv = grade_gpv * course_credit
            cc_gpvs.append(cc_gpv)
            total_credits.append(course_credit)

    if sum(cc_gpvs) == 0 or sum(total_credits) == 0:
        gpa = 0
    else:
        gpa = round(sum(cc_gpvs)/sum(total_credits),2)

    year_gpa_dict = {year: gpa}

    return year_gpa_dict

def gpa_classification(overall_gpa):
    if overall_gpa >= 3.75:
        return "Distinction"
    elif overall_gpa < 3.75 and overall_gpa >= 3.25:
        return "Merit"
    elif overall_gpa < 3.25 and overall_gpa >= 2.68:
        return "Credit"
    elif overall_gpa > 2.68 and overall_gpa >= 0:
        return "Credit"
    else:
        return ""
