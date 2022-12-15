# Import pandas
import pandas as pd
import matplotlib.pyplot as plt

# Load the data into  3 DataFrames
medical_records = pd.read_csv("data/cases_medical.txt", delimiter="\t", header=0)
personal_information = pd.read_csv("data/cases_personal.txt", delimiter="\t", header=0)
stroke_codes = pd.read_csv("data/stroke_codes.txt", delimiter="\t", header=0)

# ---- 1/ Add the patients’ personal information to each of their enhanced medical records ---- #
# ---- I will use the merge function to combine the two dataframes because they share the patient number column ---- #
enhanced_medical_records = pd.merge(medical_records, personal_information, on='idno')

# ---- 2/ Generate a binary variable for each enhanced medical record to indicate whether it is a stroke record ---- #
# ---- I will transform the stroke code to a list first ---- #
all_strokes = stroke_codes['medcode'].values.tolist()
# ---- Create a new binary column that takes 1 if it is a stroke and 0 otherwise ---- #
# ---- I will use the isin function to check if the medcode corresponds to one of the stroke codes---- #
enhanced_medical_records['is_stroke'] = enhanced_medical_records['medcode'].isin(all_strokes).map({True: 1, False: 0})

# ---- 3/ Generate a variable in each enhanced medical record to indicate age at first stroke for that patient. ---- #
# ---- Step 1: This section of the tasks involves comparing dates, so first I convert them to datetime ---- #
enhanced_medical_records["evntdate"] = pd.to_datetime(enhanced_medical_records["evntdate"], format="%d%b%Y")
enhanced_medical_records["dob"] = pd.to_datetime(enhanced_medical_records["dob"], format="%d%b%Y")
# ---- Step 2: Filter the dataframe to only include records where "is_stroke" is 1. ---- #
strokes = enhanced_medical_records[enhanced_medical_records["is_stroke"] == 1]
# ---- Step 3: Sort the stroke dataframe by evntdate in ascending order ---- #
# ---- This is to ensure that the first row in the filtered dataframe is when the patient had their first strike ---- #
strokes = strokes.sort_values(by="evntdate")


# ---- Step 4: Create a function that calculates the age of patient when they had their first stroke in years. ---- #
# ---- We round the age to avoid having decimals. ---- #
def calculate_age(row):
    if row["evntdate"] < row["dob"]:
        age = 0
    else:
        age = int((row["evntdate"] - row["dob"]).total_seconds() / (3600 * 24 * 365.25))
    return age


# ---- Step 5: Apply the function to the strokes dataframe. ---- #.
strokes["age_at_first_stroke"] = strokes.apply(calculate_age, axis=1)
# ---- Step 6: Create the new column in the enhanced medical records ---- #.
# ---- Create a dictionary that maps patient_id to age_at_first_stroke ---- #.
age_map = dict(zip(strokes["idno"], strokes["age_at_first_stroke"]))
# ---- Create the ae at first stroke in the enhanced records and fill it using the map dictionary we created ---- #.
enhanced_medical_records["age_at_first_stroke"] = enhanced_medical_records["idno"].map(age_map)

# Print the resulting dataframe to see the combined data
print(enhanced_medical_records)
# ---- Data enhancement complete! ---- #

# ---- Summary theme 1: The personal information of the study population ---- #
# ---- Sex summary ---- #
plt.pie(
    # Generate data
    [
        # Number of males
        len(personal_information[personal_information['sex'] == 1]),
        # Number of females
        len(personal_information[personal_information['sex'] == 2]),
    ],
    # Labels for the pie chart
    labels=['Males', 'Females'],
    # Add a percentage label to each slice
    autopct='%1.1f%%'
)
# Add a title
plt.title('Gender Distribution')
# Show the chart
plt.show()

# ---- age summary ---- #
# ---- To summarize the age, we have to add a column for age to the personal information  ---- #
personal_information['year'] = pd.to_datetime(personal_information['dob']).dt.year
year_counts = personal_information.groupby('year')['year'].count()
plt.plot(year_counts.index, year_counts.values)
plt.xlabel('Year of birth')
plt.ylabel('Number of Patients')
plt.title('Number of patients by Year of birth')
plt.show()

# ---- Stroke summary ---- #
# ---- I will work on the first_stroke dataframe that I previously created ---- #
# ---- Remove rows where age at first stroke is 0  ---- #
strokes = strokes.drop(strokes[strokes['age_at_first_stroke'] == 0].index)
# ---- Replace the genders with meaningful words for the chart  ---- #
strokes['sex'] = strokes['sex'].replace({1: 'Male', 2: 'Female'})
###################### Chart creations ######################
# Create a bar chart showing the number of strokes by gender
strokes.groupby('sex')['is_stroke'].sum().plot(kind='bar', rot=0)
plt.xlabel('Gender')
plt.ylabel('Number of Strokes')
plt.show()

# Create a histogram showing the distribution of age at first stroke
strokes['age_at_first_stroke'].plot(kind='hist')
plt.xlabel('Age at First Stroke')
plt.ylabel('Number of Patients')
plt.show()

#### Stroke descriptions ###
# ---- I will create a dictionary for each description and its occurrence ---- #
descriptions = strokes['description'].value_counts().to_dict()
# ---- Sort the occurrences and get the top 3 occurring ones ---- #
top_3 = sorted(descriptions.items(), key=lambda x: x[1], reverse=True)[:3]
# get the keys and values from the dictionary
x_values = [x[0] for x in top_3]
y_values = [x[1] for x in top_3]
plt.barh(x_values, y_values)
plt.show()
