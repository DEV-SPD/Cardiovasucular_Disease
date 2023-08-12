import pandas as pd
import streamlit as st
import pickle
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder()

with open('HEART_DISEASE','rb') as f:
    model = pickle.load(f)

def suggest_treatment_by_age(age):
    treatment_suggestions = []

    if age >= 20 and age <= 35:
        treatment_suggestions.append("Focus on establishing a healthy lifestyle:")
        treatment_suggestions.append("-->Regular physical activity")
        treatment_suggestions.append("-->Balanced diet with whole grains, lean proteins, fruits, and vegetables")
        treatment_suggestions.append("-->Avoid smoking and limit alcohol consumption")
        treatment_suggestions.append("--Regular health check-ups and monitoring")

    elif age >= 35 and age <= 60:
        treatment_suggestions.append("Manage cardiovascular risk factors:")
        treatment_suggestions.append("- Monitor and manage blood pressure")
        treatment_suggestions.append("- Cholesterol management, possibly with statins")
        treatment_suggestions.append("- Diabetes management if applicable")
        treatment_suggestions.append("- Consider low-dose aspirin under medical guidance")
        treatment_suggestions.append("- Continue healthy lifestyle habits")

    elif age >= 60:
        treatment_suggestions.append("Continue managing heart health:")
        treatment_suggestions.append("- Monitor and manage blood pressure, cholesterol, and blood sugar")
        treatment_suggestions.append("- Medications to manage heart conditions, as prescribed")
        treatment_suggestions.append("- Regular heart screenings and tests")
        treatment_suggestions.append("- Maintain healthy lifestyle habits and make necessary adjustments")
        treatment_suggestions.append("- Collaborate closely with healthcare providers, including cardiologists")

    else:
        treatment_suggestions.append("For personalized advice, please consult a healthcare professional.")

    return treatment_suggestions

def a(age):
    suggested_treatment = suggest_treatment_by_age(age)
    for suggestion in suggested_treatment:
        print(suggestion)
def main():
    st.title('CARDIOVASCULAR DISEASE DIAGNOSIS')

    age = st.text_input('ENTER YOUR AGE: ')
    sex = st.text_input('ENTER YOUR GENDER:')
    cp  = st.selectbox('SELECT CHEST PAIN TYPE: ',['SELECT','Typical Angina','Atypical Angina','Non-Angina','Asymptomatic'])
    trestbps = st.text_input('ENTER REST BLOOD PRESSURE: ')
    chol = st.text_input('ENTER SERUM CHOLESTROL (Mg/dl) : ')
    fbs = st.text_input('FASTING BLOOD PRESSURE: ')
    restecg = st.selectbox('ENTER ELECTROCARDIOGRAPHIC RESULTS: ',['SELECT','Normal', 'Stt Abnormality', 'Lv Hypertrophy'])
    thalach = st.text_input('ENTER MAXIMUM HEART RATE ACHIEVED: ')
    exang = st.selectbox('EXERCISE INDUCED ANGINA?',['SELECT','YES', 'NO'])
    oldpeak = st.text_input('ST DEPRESSION INDUCED BY EXERCISE RELATIVE TO REST:')
    slope = st.text_input('THE SLOPE OF THE PEAK EXERCISE ST SEGMENT:')
    ca = st.text_input('NUMBER OF MAJOR VESSELS (0-3) COLORED BY FLOUROSOPY:')
    thal = st.selectbox('THAL:', ['SELECT','NORMAL', 'FIXED DEFECT', 'REVERSIBLE DEFECT'])

    dict = {
        'age':[age],
        'sex':[sex],
        'cp':[cp],
        'trestbps':[trestbps],
        'chol':[chol],
        'fbs':[fbs],
        'restecg':[restecg],
        'thalach':[thalach],
        'exang':[exang],
        'oldpeak':[oldpeak],
        'slope': [slope],
        'ca':[ca],
        'thal':[thal],
    }

    df = pd.DataFrame(dict)

    df['cp'] = encoder.fit_transform(df['cp'])
    df['sex'] = encoder.fit_transform(df['sex'])
    df['restecg'] = encoder.fit_transform(df['restecg'])
    df['exang'] = encoder.fit_transform(df['exang'])
    df['thal'] = encoder.fit_transform(df['thal'])

    if st.button('PREDICT'):
      result = model.predict(df)
      if(result==1):
        st.error("The AI model suggests a slightly higher likelihood of a heart-related concern based on the following factors.")
        suggested_treatment = suggest_treatment_by_age(int(age))
        st.info("Heart Concern Treatment Suggestions:")
        for suggestion in suggested_treatment:
            st.info(suggestion)
      else:
        st.success('The AI model indicates a relatively lower risk of a heart-related concern due to the following factors.')



if __name__ == '__main__':
    main()