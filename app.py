import numpy as np
import pandas as pd
import pickle


import matplotlib.pyplot as plt
import seaborn as sns


import streamlit as st


bac_list_refined = ['Staphylococcus aureus', 'Escherichia coli',
                    'Klebsiella pneumoniae', 'Staphylococcus epidermidis',
                    'Pseudomonas aeruginosa']

ab = {'Staphylococcus aureus': ['Penicillin', 'Ceftriaxone', 'Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime',
                                'Cotrimoxazole', 'Meropenem', 'Amoxicillin-Clavulanic acid', 'Imipenem', 'Gentamicin',
                                'Clindamycin', 'Ampicillin-Amoxicillin', 'Erythromycin', 'Tetracycline', 'Cefuroxime',
                                'Cefazolin', 'Oxacillin', 'Fusidic acid'],
      'Escherichia coli': ['Ceftriaxone', 'Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime', 'Cotrimoxazole',
                           'Amoxicillin-Clavulanic acid', 'Tobramycin', 'Ceftazidime', 'Levofloxacin', 'Amikacin',
                           'Ampicillin-Amoxicillin', 'Ertapenem', 'Norfloxacin', 'Cefpodoxime'],
      'Klebsiella pneumoniae': ['Ceftriaxone', 'Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime', 'Cotrimoxazole',
                                'Amoxicillin-Clavulanic acid', 'Tobramycin', 'Ceftazidime', 'Levofloxacin', 'Ertapenem',
                                'Fosfomycin-Trometamol', 'Norfloxacin', 'Cefpodoxime'],
      'Staphylococcus epidermidis': ['Ceftriaxone', 'Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime',
                                     'Cotrimoxazole', 'Meropenem', 'Amoxicillin-Clavulanic acid', 'Imipenem',
                                     'Gentamicin', 'Clindamycin', 'Erythromycin', 'Tetracycline', 'Rifampicin',
                                     'Cefuroxime', 'Cefazolin', 'Oxacillin', 'Fusidic acid'],
      'Pseudomonas aeruginosa': ['Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime', 'Meropenem', 'Colistin',
                                 'Tobramycin', 'Ceftazidime', 'Levofloxacin', 'Imipenem', 'Aztreonam']}




def plot_ab(shap_vals, spec_ab):
  with st.spinner('Пожалуйста, подождите...'):
    std = np.std(shap_vals)
    mean = np.mean(shap_vals)
    list_for_plots = []
    for i in range(len(shap_vals)):
        list_for_plots.append((shap_vals[i], i, spec_ab[i]))
    sns.set_style("darkgrid")
    fig1, ax = plt.subplots(figsize=(22, 5))
    ax.set_xlabel('m/z')
    ax.set_ylabel('Значимость')
    ax.set_title('График степени влияния пиков на результат модели')


    ax.bar(x=[k[1] for k in list_for_plots if np.abs(k[0]) > (mean + (2 * std))],
            height=[k[0] for k in list_for_plots if np.abs(k[0]) > (mean + (2 * std))], width=0.01,
            edgecolor='mediumaquamarine')
    ax.bar(x=[k[1] for k in list_for_plots if np.abs(k[0]) < (mean + (2 * std))],
            height=[k[0] for k in list_for_plots if np.abs(k[0]) < (mean + (2 * std))],
            width=0.01, alpha=0.6, edgecolor='grey')
    ax.set_xticks(np.arange(min(range(len(list_for_plots))), max(range(len(list_for_plots))) + 1, 200.0))
    #plt.show()
    st.pyplot(fig1)


    sns.set_style("darkgrid")
    fig2, ax = plt.subplots(figsize=(22, 5))
    spec_ab_plt = spec_ab
    ax.plot(range(spec_ab_plt.shape[0]), spec_ab_plt, color='indigo')
    ax.set_xticks(np.arange(min(range(spec_ab_plt.shape[0])), max(range(spec_ab_plt.shape[0])) + 1, 200.0))
    ax.set_xlabel("m/z")
    ax.set_ylabel("Интенсивность")
    ax.set_title('Спектр')
    st.pyplot(fig2)

    






bac_strain_dict = {3: 'Staphylococcus aureus', 0: 'Escherichia coli',
                    1: 'Klebsiella pneumoniae', 4: 'Staphylococcus epidermidis',
                    2: 'Pseudomonas aeruginosa'}

antibiotic_dict = {'Staphylococcus aureus': ['Penicillin', 'Ceftriaxone', 'Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime',
                                'Cotrimoxazole', 'Meropenem', 'Amoxicillin-Clavulanic acid', 'Imipenem', 'Gentamicin',
                                'Clindamycin', 'Ampicillin-Amoxicillin', 'Erythromycin', 'Tetracycline', 'Cefuroxime',
                                'Cefazolin', 'Oxacillin', 'Fusidic acid'],
      'Escherichia coli': ['Ceftriaxone', 'Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime', 'Cotrimoxazole',
                           'Amoxicillin-Clavulanic acid', 'Tobramycin', 'Ceftazidime', 'Levofloxacin'],
      'Klebsiella pneumoniae': ['Ceftriaxone', 'Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime', 'Cotrimoxazole',
                                'Amoxicillin-Clavulanic acid', 'Tobramycin', 'Ceftazidime', 'Levofloxacin'],
      'Staphylococcus epidermidis': ['Ceftriaxone', 'Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime',
                                     'Cotrimoxazole', 'Meropenem', 'Amoxicillin-Clavulanic acid', 'Imipenem',
                                     'Gentamicin', 'Clindamycin', 'Erythromycin', 'Tetracycline', 'Rifampicin',
                                     'Cefuroxime', 'Cefazolin', 'Oxacillin', 'Fusidic acid'],
      'Pseudomonas aeruginosa': ['Piperacillin-Tazobactam', 'Ciprofloxacin', 'Cefepime', 'Meropenem', 'Colistin',
                                 'Tobramycin', 'Ceftazidime', 'Levofloxacin', 'Imipenem', 'Aztreonam']}


resistance_res_dict = {1: 'S', 0: 'R'}






def color_resist(val):
    if val == 'S':
        color = 'lightgreen'
    else:
        color = 'red'
    return f'background-color: {color}'








st.title("MALDIScan")
st.subheader("Демо версия")

st.write("В демо версии спектр уже загружен")
st.write("Загружен файл: test_spectrum.csv")
if 'run' not in st.session_state:
    st.session_state.run = False

def change_state():
    st.session_state.run = not st.session_state.run

def change_state2():
    st.session_state.interpret = not st.session_state.interpret

st.button('Начать анализ', on_click=change_state)
if st.session_state.run:
    st.write('Определяем штамм бактерии и устойчивость...')
    strain = 'Staphylococcus aureus'
    shap_ab_dict = pickle.load(open("st_au_shap_dict.pkl", "rb"))
    df = pd.read_pickle("st_au_df.pkl")
    st.write("Штамм бактерии: ", strain)
    st.dataframe(df.style.applymap(color_resist, subset=['Результат']))
    if 'interpret' not in st.session_state:
        st.session_state['interpret'] = False
    st.button('Интерпретировать', on_click=change_state2)
    if st.session_state.interpret:
        option = st.selectbox(
        'Для интерпретации результата для конкретного антибиотика выберите его из списка',antibiotic_dict[strain]
        )
        spec_ab = pickle.load(open("spec_ab.pickle", "rb"))
        plot_ab(shap_ab_dict[option], spec_ab)
