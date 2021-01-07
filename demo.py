import os
with open(os.path.join('C:/Users/MACHENIKE/Desktop/MDS/Big Data Application and Analytics/Assignment/SVD_Recommender-main','Procfile'), "w") as file1:
    toFile = 'web: sh setup.sh && streamlit run test_apps.py'
    
file1.write(toFile)