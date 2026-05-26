import numpy as np
import pandas as pd

np.random.seed(42)
N = 918

age = np.random.normal(54, 9, N).clip(28, 77).astype(int)
sex = np.random.choice([0, 1], N, p=[0.32, 0.68])
chest_pain = np.random.choice([0, 1, 2, 3], N, p=[0.08, 0.17, 0.28, 0.47])
resting_bp = np.random.normal(132, 18, N).clip(94, 200).astype(int)
cholesterol = np.random.normal(244, 52, N).clip(126, 564).astype(int)

fasting_bs = np.where(
    age > 55,
    np.random.choice([0,1], N, p=[0.72,0.28]),
    np.random.choice([0,1], N, p=[0.85,0.15])
)

resting_ecg = np.random.choice([0, 1, 2], N, p=[0.60, 0.19, 0.21])

max_hr = (
    220 - age - np.random.normal(0, 12, N)
).clip(60, 202).astype(int)

exercise_angina = np.where(
    chest_pain == 3,
    np.random.choice([0,1], N, p=[0.45,0.55]),
    np.random.choice([0,1], N, p=[0.82,0.18])
)

oldpeak = np.random.exponential(1.0, N).clip(0, 6.2).round(1)

st_slope = np.random.choice([0, 1, 2], N, p=[0.32, 0.47, 0.21])

risk_score = (
    (age > 55).astype(int) * 0.3 +
    (sex == 1).astype(int) * 0.2 +
    (chest_pain == 3).astype(int) * 0.5 +
    (resting_bp > 140).astype(int) * 0.2 +
    (cholesterol > 240).astype(int) * 0.15 +
    (fasting_bs == 1).astype(int) * 0.25 +
    (exercise_angina == 1).astype(int) * 0.4 +
    (oldpeak > 2).astype(int) * 0.3 +
    (st_slope == 1).astype(int) * 0.25 +
    np.random.normal(0, 0.2, N)
)

target = (risk_score > 1.0).astype(int)

df = pd.DataFrame({
    'Age': age,

    'Sex': pd.Categorical(
        np.where(sex == 1, 'Male', 'Female')
    ),

    'ChestPainType': pd.Categorical(
        np.select(
            [
                chest_pain==0,
                chest_pain==1,
                chest_pain==2,
                chest_pain==3
            ],
            [
                'Typical Angina',
                'Atypical Angina',
                'Non-Anginal Pain',
                'Asymptomatic'
            ],
            default='Asymptomatic'
        )
    ),

    'RestingBP': resting_bp,

    'Cholesterol': cholesterol,

    'FastingBS': fasting_bs,

    'RestingECG': pd.Categorical(
        np.select(
            [
                resting_ecg==0,
                resting_ecg==1,
                resting_ecg==2
            ],
            [
                'Normal',
                'ST',
                'LVH'
            ],
            default='Normal'
        )
    ),

    'MaxHR': max_hr,

    'ExerciseAngina': pd.Categorical(
        np.where(exercise_angina==1,'Yes','No')
    ),

    'Oldpeak': oldpeak,

    'ST_Slope': pd.Categorical(
        np.select(
            [
                st_slope==0,
                st_slope==1,
                st_slope==2
            ],
            [
                'Up',
                'Flat',
                'Down'
            ],
            default='Flat'
        )
    ),

    'HeartDisease': target
})

df.to_csv('heart_disease_data.csv', index=False)

print(f"Dataset saved: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Heart disease prevalence: {df['HeartDisease'].mean():.1%}")