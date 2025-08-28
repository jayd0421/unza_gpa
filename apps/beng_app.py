import streamlit as st
import pandas as pd
from apps import beng_functions

# Import dataset
data = pd.read_csv('data/gpa_data.csv')

# List of possible grades
grades_list = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'P', 'S']

def app():
    # Set title
    st.title('UNZA BEng GPA Calculator')

    # Get list of beng departments
    departments_list = beng_functions.departments_list(data)

    # Select department using radio
    selected_department = st.radio(
        "Select department", 
        departments_list,
        index=None,
        horizontal=True
        )

    if selected_department:
        # Display selected department as a header
        st.header(f"{selected_department} Engineering GPA")

        # Add radio with specializations if EEE department selected
        if selected_department == 'Electrical & Electronics':
            electrical_specialty = st.radio(
                "Select specialisation",
                ["Electrical Machines and Power", "Electronics and Telecommunication"],
                0,
                horizontal=True)

        gpa_col, grade_col = st.columns([1, 7])

        with grade_col:
            # Choose if first year results should be added
            include_first_year = st.toggle(
                "Include 1st year results?",
                True
                )
            
            # Study years if first year toggle on
            if include_first_year:
                years_list = beng_functions.years_of_study_list(data)

            # Study years if first year toggle off
            else:
                years_list = beng_functions.years_of_study_list(data)
                years_list = years_list[1:]

            # Year grades in list
            overall_grades = {}

            years_gpa_dict = {}

            # Get courses for each year
            for year in years_list:
                # Create expander for each year
                with st.expander(f"{year} year"):

                    # Get df for specific year and department
                    department_df = beng_functions.department_df(
                        data, selected_department, year
                        )

                    # Electrical speciality set to None if selected department not EEE
                    if selected_department != 'Electrical & Electronics':
                        electrical_specialty = None

                    # Get compulsory and elective courses dict
                    compulsory_courses_dict, elective_courses_dict = beng_functions.courses_dict(
                        selected_department, department_df, electrical_specialty)

                    year_courses_grade_dict = {}
                    iteration = 0
                    if len(compulsory_courses_dict) > 0:
                        # Heading for compulsory courses
                        st.markdown(":red-background[Compulsory Courses]")

                        # Create 2 columns to hold the data input 
                        col1, col2 = st.columns([1,1])

                        # Iterate through compulsory courses
                        for (course_code, course_name) in compulsory_courses_dict.items():
                            # Keep track of the iteration
                            iteration = iteration + 1

                            # Odd data iteration added to the left column
                            if iteration % 2 != 0:
                                with col1:
                                    grade = st.radio(
                                        label=f"{course_code} - {course_name}",
                                        options=grades_list,
                                        index=None,
                                        horizontal=True,
                                        key=course_code)

                            # Even data iteration added to the right column
                            else:
                                with col2:
                                    grade = st.radio(
                                        label=f"{course_code} - {course_name}",
                                        options=grades_list,
                                        index=None,
                                        horizontal=True,
                                        key=course_code)

                            # Course code and grade as dictionary
                            course_grade_dict = {course_code:grade}

                            # Add course code and grade to main dictionary
                            year_courses_grade_dict.update(course_grade_dict)

                    if len(elective_courses_dict) > 0:
                        # Separate compulsory from elective courses
                        st.divider()

                        # Heading for elective courses
                        st.markdown(":red-background[Elective Courses]")

                        # Create 2 columns to hold the data input
                        col1, col2 = st.columns([1,1])

                        # Iterate through elective courses
                        for (course_code, course_name) in elective_courses_dict.items():
                            # Keep track of the iteration
                            iteration = iteration + 1

                            # Odd iteration data added to left column
                            if iteration % 2 != 0:
                                with col1:
                                    grade = st.radio(
                                        label=f"{course_code} - {course_name}",
                                        options=grades_list,
                                        index=None,
                                        horizontal=True,
                                        key=course_code)

                            # Even iteration data added to the right column
                            else:
                                with col2:
                                    grade = st.radio(
                                        label=f"{course_code} - {course_name}",
                                        options=grades_list,
                                        index=None,
                                        horizontal=True,
                                        key=course_code)

                            # Course code and grade as dictionary
                            course_grade_dict = {course_code:grade}

                            # Add course code and grade to main dictionary
                            year_courses_grade_dict.update(course_grade_dict)

                    courses_grade_dict = {year: year_courses_grade_dict}

                overall_grades.update(courses_grade_dict)

                course_credits_dict = beng_functions.course_credits_dict(
                    selected_department, department_df, electrical_specialty)

                year_gpa_dict = beng_functions.year_gpa(
                    overall_grades, course_credits_dict, year)

                years_gpa_dict.update(year_gpa_dict)


        with gpa_col:
            if sum(years_gpa_dict.values()) != 0:
                gpas = years_gpa_dict.values()
                overall_gpa = round(sum(gpas)/len([gpa for gpa in gpas if gpa > 0]), 3)

                gpa_classification = beng_functions.gpa_classification(overall_gpa)

                with st.container(border=True):
                    st.metric(
                        label="Overall GPA",
                        value=overall_gpa,
                    )
                    if gpa_classification == "Distinction":
                        st.markdown(f":green-background[{gpa_classification}]")
                    elif gpa_classification == "Merit":
                        st.markdown(f":yellow-background[{gpa_classification}]")
                    elif gpa_classification == "Credit":
                        st.markdown(f":white-background[{gpa_classification}]")
                    elif gpa_classification == "Pass":
                        st.markdown(f":red-background[{gpa_classification}]")

            with st.container(border=True):
                if include_first_year:
                    st.metric(
                        label="First Year GPA",
                        value=years_gpa_dict['First'],
                    )

                st.metric(
                    label="Second Year GPA",
                    value=years_gpa_dict['Second'],
                )

                st.metric(
                    label="Third Year GPA",
                    value=years_gpa_dict['Third'],
                )

                st.metric(
                    label="Fourth Year GPA",
                    value=years_gpa_dict['Fourth'],
                )

                st.metric(
                    label="Fifth Year GPA",
                    value=years_gpa_dict['Fifth'],
                )
