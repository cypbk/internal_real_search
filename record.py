import streamlit as st
import numpy as np
import random
import pandas as pd
import re


@st.cache_data
def generate_list():
    result = []
    while len(result) < 4:
        num = random.randint(1, 4)
        if num not in result and len(result) + 1 != num:
            result.append(num)
    return result

def generate_display(t_round):
    array_memory_num = np.empty((8, 1), dtype='int')
    # color of search word
    array_color = np.empty((8, 1), dtype='object')
    # color to be memorized
    array_memory = np.empty((8, 1), dtype='object')
    array_memory_out = np.empty((8, 1), dtype='object')
    array_shade_num = np.empty((8, 1), dtype='int')
    array_shade = np.empty((8,1), dtype='object')
    array_target = np.empty((8,1), dtype='object')


    dict_1 = {'blue_1':'Tale',
              'blue_2':'Across',
              'blue_3':'Diary',
              'yellow_1':'Whisper',
              'yellow_2':'Global',
              'yellow_3':'Pen',
              'green_1':'Beyond',
              'green_2':'Political',
              'green_3':'Through',
              'red_1':'Explore',
              'red_2':'Yesterday',
              'red_3':'Creativity'
              }

    dict_2 = {'blue_1':'Teaching',
              'blue_2':'Messages',
              'blue_3':'Journey',
              'yellow_1':'Passport',
              'yellow_2':'Universe',
              'yellow_3':'Maze',
              'green_1':'Science',
              'green_2':'Classroom',
              'green_3':'Travel',
              'red_1':'Quest',
              'red_2':'Hidden',
              'red_3':'Curve'
              }
    
    dict_3 = {'blue_1':'Understand',
              'blue_2':'Core',
              'blue_3':'Ride',
              'yellow_1':'Office',
              'yellow_2':'Wellness',
              'yellow_3':'Voice',
              'green_1':'Business',
              'green_2':'Human',
              'green_3':'Showcase',
              'red_1':'Leaders',
              'red_2':'Body',
              'red_3':'Stage'
              }
    
    dict_e = {'blue_1':'',
              'blue_2':'',
              'blue_3':'',
              'yellow_1':'',
              'yellow_2':'',
              'yellow_3':'',
              'green_1':'',
              'green_2':'',
              'green_3':'',
              'red_1':'',
              'red_2':'',
              'red_3':''
              }

    if t_round == 1:
        target_dict = dict_1
    elif t_round == 2:
        target_dict = dict_2
    elif t_round == 3:
        target_dict = dict_3
    else:
        target_dict = dict_e
    
    data_column_1 = np.tile(np.arange(1, 5), 2)
    array_color[data_column_1 == 1] = 'blue'
    array_color[data_column_1 == 2] = 'red'
    array_color[data_column_1 == 3] = 'green'
    array_color[data_column_1 == 4] = 'yellow'

    notmatch_list = generate_list()
    #print(notmatch_list)
    array_temp = np.zeros((8,1), dtype='int')
    for i in range(8):
        if i < 4:
            array_temp[i,0]= i+1
        else:
            array_temp[i,0]= notmatch_list[i-4]

    array_memory[array_temp == 1] = 'blue'
    array_memory[array_temp == 2] = 'red'
    array_memory[array_temp == 3] = 'green'
    array_memory[array_temp == 4] = 'yellow'

    for i in range(4):
        random_numbers = random.sample([1, 2, 3], 2)
        array_shade_num[i,0] = random_numbers[0]
        array_shade_num[i+4,0] = random_numbers[1]
        
        random_numbers_memory = random.sample([1, 2, 3], 2)
        array_memory_num[i,0] = random_numbers_memory[0]
        array_memory_num[i+4,0] = random_numbers_memory[1]

    for i in range(8):
        array_memory_out[i,0] = f'{array_memory[i,0]}_{array_memory_num[i,0]}'
        array_shade[i,0] = f'{array_color[i,0]}_{array_shade_num[i,0]}'
        array_target[i,0] = target_dict[array_shade[i,0]]

    seen = set()
    for i, element in np.ndenumerate(array_memory_out):
        match = re.match(r'(\w+_)(\d)', element)
        if match:
            prefix, number = match.groups()
            if element in seen:
                new_number = str((int(number) % 3) + 1)  # 修改第二个重复元素的数字，确保在1到3的范围内且不同于第一个重复元素
                array_memory_out[i] = prefix + new_number
            else:
                seen.add(element)
    
    
    array_final = np.hstack((array_memory_out, array_shade, array_target))
    
    #print(array_final)    
    np.random.shuffle(array_final)
    #print(array_final)

    data = {
        'Memory_color': array_final[:,0],
        'Target_color': array_final[:,1],
        'Target_word': array_final[:,2],
    }

    df_display = pd.DataFrame(data)
    
    df_display['RT'] = np.nan
    
    return df_display

def set_trials():
    st.session_state['clicked'] = True
    st.session_state['df'] = generate_display(t_round)

st.sidebar.header('Participant information')
p_id = st.sidebar.text_input('Participant ID', 'test')
gender_options = ['unknow', 'female', 'male']
p_gender = st.sidebar.selectbox('Participant gender', gender_options)
p_age = st.sidebar.text_input('Participant age', '999')
round_options = [0, 1, 2, 3]
st.session_state['round'] = st.sidebar.selectbox(label = 'Round', options= round_options, index= 0)
st.sidebar.button(label='Set Trials', on_click = set_trials)

# body
# Initialization
if 'clicked' not in st.session_state:
    st.session_state['clicked'] = False

if 'round' not in st.session_state:
    st.session_state['round'] = 0

t_round = st.session_state['round']

if 'df' not in st.session_state:
    st.session_state['df'] = generate_display(t_round)
    
st.title('Trial information')
edited_df = st.data_editor(st.session_state['df'], hide_index=True, 
                           use_container_width=True, 
                           disabled=['Memory_color', 'Target_shade', 'Target_word'])

st.download_button('Download trial information as .csv', edited_df.to_csv(index=False), 
                f'data_{p_id}_{p_gender}_{p_age}_r{t_round}.csv',
                use_container_width=True)
