import streamlit as st
import pandas as pd
from apps import beng_functions

# Import dataset
data = pd.read_csv('data/gpa_data.csv')

# List of possible grades
grades_list = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'P', 'F', 'S']

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

        if selected_department == 'Electrical & Electronics':
            eletrical_specialty = st.radio(
                "Select specialisation",
                ["Electrical Machines and Power", "Electronics and Telecommunication"],
                0,
                horizontal=True)

        # Choose if first year results should be added
        include_first_year = st.toggle(
            "Include 1st year results?",
            True
            )

        if include_first_year:
            years_list = beng_functions.years_of_study_list(data)
        else:
            years_list = beng_functions.years_of_study_list(data)
            years_list = years_list[1:]

        for year in years_list:
            with st.expander(f"{year} year"):

                department_df = beng_functions.department_df(
                    data, selected_department, year
                    )

                if selected_department == 'Electrical & Electronics':
                    eletrical_specialties_dict = {
                        "Electrical Machines and Power": 'ET', 
                        "Electronics and Telecommunication": "EMP"}

                    department_df = department_df[
                        department_df['comment'] != eletrical_specialties_dict[eletrical_specialty]
                        ]

                    compulsory_courses_dict = dict(zip(
                        department_df[department_df['is_compulsory'] == 1]['course_code'],
                        department_df[department_df['is_compulsory'] == 1]['course']
                        ))

                    elective_courses_dict = dict(zip(
                        department_df[department_df['is_compulsory'] == 0]['course_code'],
                        department_df[department_df['is_compulsory'] == 0]['course']
                        ))

                else:
                    compulsory_courses_dict = dict(zip(
                        department_df[department_df['is_compulsory'] == 1]['course_code'],
                        department_df[department_df['is_compulsory'] == 1]['course']
                        ))

                    elective_courses_dict = dict(zip(
                        department_df[department_df['is_compulsory'] == 0]['course_code'],
                        department_df[department_df['is_compulsory'] == 0]['course']
                        ))

                iteration = 0
                if len(compulsory_courses_dict) > 0:
                    st.markdown(":red-background[Compulsory Courses]")
                    col1, col2 = st.columns([1,1])
                    for (course_code, course_name) in compulsory_courses_dict.items():
                        iteration = iteration + 1
                        if iteration % 2 != 0:
                            with col1:
                                grade = st.radio(
                                    label=f"{course_code} - {course_name}",
                                    options=grades_list,
                                    index=None,
                                    horizontal=True,
                                    key=course_code)
                        else:
                            with col2:
                                grade = st.radio(
                                    label=f"{course_code} - {course_name}",
                                    options=grades_list,
                                    index=None,
                                    horizontal=True,
                                    key=course_code)

                if len(elective_courses_dict) > 0:
                    st.divider()
                    st.markdown(":red-background[Elective Courses]")
                    col1, col2 = st.columns([1,1])
                    for (course_code, course_name) in elective_courses_dict.items():
                        iteration = iteration + 1
                        if iteration % 2 != 0:
                            with col1:
                                grade = st.radio(
                                    label=f"{course_code} - {course_name}",
                                    options=grades_list,
                                    index=None,
                                    horizontal=True,
                                    key=course_code)
                        else:
                            with col2:
                                grade = st.radio(
                                    label=f"{course_code} - {course_name}",
                                    options=grades_list,
                                    index=None,
                                    horizontal=True,
                                    key=course_code)
