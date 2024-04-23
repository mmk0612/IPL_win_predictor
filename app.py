import streamlit as st 
import pickle
import pandas as pd

pipe = pickle.load(open('pipe.pkl','rb'))

teams = ['Rajasthan Royals', 'Delhi Capitals',
       'Royal Challengers Bangalore', 'Gujarat Titans',
       'Chennai Super Kings', 'Sunrisers Hyderabad', 'Punjab Kings',
       'Kolkata Knight Riders', 'Mumbai Indians', 'Lucknow Super Giants']

venues =['Rajiv Gandhi International Stadium, Uppal, Hyderabad',
       'Wankhede Stadium, Mumbai', 'Arun Jaitley Stadium, Delhi',
       'Shaheed Veer Narayan Singh International Stadium',
       'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow',
       'Eden Gardens, Kolkata',
       'Himachal Pradesh Cricket Association Stadium, Dharamsala',
       'M Chinnaswamy Stadium, Bengaluru',
       'Dr DY Patil Sports Academy, Mumbai',
       'MA Chidambaram Stadium, Chepauk, Chennai',
       'Sawai Mansingh Stadium, Jaipur', 
       'Narendra Modi Stadium, Ahmedabad',
       'JSCA International Stadium Complex',
       'Punjab Cricket Association Stadium, Mohali',
       'Brabourne Stadium, Mumbai',
       'Maharashtra Cricket Association Stadium, Pune',
       'Sardar Patel Stadium, Motera',
       'Saurashtra Cricket Association Stadium', 'Barabati Stadium',
       'Vidarbha Cricket Association Stadium, Jamtha',
       'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur',
       'Green Park', 'Barsapara Cricket Stadium, Guwahati',
       'Holkar Cricket Stadium'
    ]


st.title('IPL Second Innings Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',teams)

with col2:
    bowling_team = st.selectbox('Select the bowling team',teams)

selected_venue = st.selectbox('Select the Venue',sorted(venues))

target = st.number_input('Enter the target score',min_value=0,step=1)

col3,col4,col5 = st.columns(3)

with col3:
    runs = st.number_input('Runs scored',min_value=0,step=1)

with col4:
    overs = st.number_input('Overs bowled',min_value=0.0,step=0.1,format="%.1f")

with col5:
    wickets = st.number_input('Wickets fallen',min_value=0,step=1)

if st.button('Predict Probability'):
    runs_left = target - runs
    curr_over = int(overs)
    curr_ball = (overs%1)*10
    ball_left = 120 - ( curr_over*6 + curr_ball )
    ball_left = int(ball_left)
    wickets_left = 10 - wickets
    crr = runs*6/((curr_over*6) + curr_ball)
    rrr = runs_left*6/ball_left

    input_df = pd.DataFrame({'Batting team':[batting_team],
                              'Bowling team':[bowling_team],
                              'Venue':[selected_venue],
                              'runs_needed':[runs_left],
                              'balls_left':[ball_left],
                              'wickets_left':[wickets_left],
                              'total_runs_x':[target],
                              'crr':[crr],
                              'rrr':[rrr]})


    print(input_df.dtypes)
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.text(batting_team + ' has ' + str(round(win*100,2)) + '% probability of winning')
    st.text(bowling_team + ' has ' + str(round(loss*100,2)) + '% probability of winning')
