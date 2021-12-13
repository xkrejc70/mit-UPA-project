from textwrap import wrap
import utils
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os import path

def load_csv(path):
    pass

def store_graph(graph, name):
    path = os.path.join(utils.graphs_dir(), f"{name}.pdf") #idk jaky extension chceme
    #store
    pass

# A1 - distribution of infected people by age in regions
def visualizeA1(name, csv_path):
    print("- " + name)
    df = pd.read_csv(csv_path)

    plt.figure()
    sns.set_theme(style="darkgrid")
    ax = sns.boxplot(x="vek", y="kraj", data=df)
    ax.tick_params(axis='y', rotation=10)
    ax.set(xlabel='Věk', ylabel='Kraj')
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+".png"))

# A2 - Series of barplots
def visualizeA2(name, csv_path):
    print("- " + name)
    df = pd.read_csv(csv_path)

    # Graph 1: total number of vaccination for each region
    sns.set_theme(style="darkgrid")

    df1 = df.groupby(['kraj_nuts_kod']).count()
    df1 = df1.reset_index()

    plt.figure()
    ax = sns.barplot(x="vekova_skupina", y="kraj_nuts_kod", data=df1)
    ax.set(xlabel='Počet naočkovaných osob', ylabel='NUTS kód kraje')
    ax.ticklabel_format(style='plain', axis='x')
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+"_1.png"))

    # Graph 2: total number of vaccination for each region divided by sex
    df2 = df.dropna(subset=['pohlavi']) 
    df2 = df2.groupby(['kraj_nuts_kod', 'pohlavi']).count()
    df2 = df2.reset_index()

    plt.figure()
    ax = sns.barplot(x="vekova_skupina", y="kraj_nuts_kod", hue='pohlavi', data=df2)
    ax.set(xlabel='Počet naočkovaných osob', ylabel='NUTS kód kraje')
    ax.ticklabel_format(style='plain', axis='x')
    
    legend = ax.get_legend()
    legend.set_title('Pohlaví')
    new_labels = ['Muži', 'Ženy']
    for t, l in zip(legend.texts, new_labels):
        t.set_text(l)

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+"_2.png"))

    # Graph 3: total number of vaccination for each region devided by three age groups (0-24, 25-59, >59)
    df3 = df.dropna(subset=['vekova_skupina'])
    # Add value to rows with nan so every row is counted
    df3 = df3.fillna('M')
    df3 = df3.groupby(['kraj_nuts_kod', 'vekova_skupina']).count()
    df3 = df3.reset_index()

    # Create list for groups
    groups_list = list()
    for index, row in df3.iterrows():
        # Devide data to 3 age groups
        if row['vekova_skupina'] == '80+':
            groups_list.append(3)
        else:
            if int(row['vekova_skupina'][-2:]) <= 24:     
                groups_list.append(1)
            elif int(row['vekova_skupina'][-2:]) <= 59:
                groups_list.append(2)
            else:
                groups_list.append(3)

    df3['skupina'] = groups_list
    df3 = df3.groupby(['kraj_nuts_kod', 'skupina']).sum()
    df3 = df3.reset_index()

    plt.figure()
    ax = sns.barplot(x="pohlavi", y="kraj_nuts_kod", hue='skupina', data=df3)
    ax.set(xlabel='Počet naočkovaných osob', ylabel='NUTS kód kraje')
    ax.ticklabel_format(style='plain', axis='x')
    ax.tick_params(axis='x', rotation=45)
    
    legend = ax.get_legend()
    legend.set_title('Věková skupina')
    new_labels = ['0-24', '25-59', '>59']
    for t, l in zip(legend.texts, new_labels):
        t.set_text(l)

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+"_3.png"))

# B - Series of covid pointers for selected region
def visualizeB(name, csv1_path, csv2_path):
    print("- " + name)
    df_cummulative = pd.read_csv(csv1_path)
    df_pop = pd.read_csv(csv2_path)

    # Keep data from last 12 months
    df_cummulative = df_cummulative.loc[(df_cummulative['datum'] >= '2020-11-30') & (df_cummulative['datum'] <= '2021-11-30')]
    
    # Get number of people in South-Moravian region
    people_in_region = df_pop.loc[(df_pop['kraj_nazev'] == 'Jihomoravský kraj')]['populace'].iloc[0]

    # Get number of people in all republic except South-Moravian region
    rest_of_people = df_pop.loc[(df_pop['kraj_nazev'] != 'Jihomoravský kraj')]['populace'].sum()
 
    df_cummulative = df_cummulative.groupby(['kraj', 'datum']).sum()
    df_cummulative = df_cummulative.reset_index()

    # Transfer cummulative data to daily
    df_cummulative = df_cummulative.sort_values(['kraj', 'datum'], ascending=[True, True])

    regions = ['Hlavní město Praha', 'Středočeský kraj', 'Jihočeský kraj', 'Plzeňský kraj', 'Karlovarský kraj', 'Ústecký kraj', 'Liberecký kraj', 'Královéhradecký kraj', 'Pardubický kraj', 'Kraj Vysočina', 'Jihomoravský kraj', 'Olomoucký kraj', 'Zlínský kraj', 'Moravskoslezský kraj]']
    daily_data = list()
    for region in regions:
        df_region = df_cummulative.loc[(df_cummulative['kraj'] == region)]
        for i in range(1, len(df_region.index)):
            daily_data.append([df_region['kraj'].iloc[i], df_region['datum'].iloc[i], df_region['kumulativni_pocet_nakazenych'].iloc[i] - df_region['kumulativni_pocet_nakazenych'].iloc[i-1], df_region['kumulativni_pocet_vylecenych'].iloc[i] - df_region['kumulativni_pocet_vylecenych'].iloc[i-1], df_region['kumulativni_pocet_umrti'].iloc[i] - df_region['kumulativni_pocet_umrti'].iloc[i-1]])
            

    df_daily = pd.DataFrame(daily_data, columns=['kraj', 'datum', 'pocet_nakazenych', 'pocet_vylecenych', 'pocet_umrti'])
    df_daily.index = pd.to_datetime(df_daily['datum'],format='%Y-%m-%d')
    df_daily = df_daily.groupby(by=[df_daily.index.month, df_daily.index.year, 'kraj']).sum()
    df_daily.index.set_names(["měsíc", "rok", "kraj"], inplace=True)
    df_daily = df_daily.reset_index()
    df_daily['měsíc'] = [ str(0)+str(month) if month < 10 else str(month) for month in df_daily["měsíc"]]
    df_daily["období"] = [str(year)+"-"+str(month) for year, month in zip(df_daily["rok"],df_daily["měsíc"])]
    df_daily = df_daily.drop(columns=['měsíc', 'rok'])

    # Group region except South-Moravian
    df_south_moravia = df_daily.loc[(df_daily['kraj'] == 'Jihomoravský kraj')]
    df_rest = df_daily.loc[(df_daily['kraj'] != 'Jihomoravský kraj')]
    df_rest = df_rest.groupby(['období']).sum()
    df_rest = df_rest.reset_index()
    df_rest['kraj'] = 'Ostatní'
    df_monthly = df_rest.append(df_south_moravia)
   
    # Normalize data
    normalized_data = list()
    for index, row in df_monthly.iterrows():
        if row['kraj'] == 'Jihomoravský kraj':
            normalized_data.append([row['kraj'], row['pocet_nakazenych']/people_in_region, row['pocet_vylecenych']/people_in_region, row['pocet_umrti']/people_in_region, row['období']])
        else:
            normalized_data.append([row['kraj'], row['pocet_nakazenych']/rest_of_people, row['pocet_vylecenych']/rest_of_people, row['pocet_umrti']/rest_of_people, row['období']])

    df_normalized = pd.DataFrame(normalized_data, columns=['kraj', 'pocet_nakazenych', 'pocet_vylecenych', 'pocet_umrti', 'období'])
    df_normalized = df_normalized.sort_values(by=['období'])

    # Graph 1: Infected persons for South-Moravian region
    plt.figure()
    ax = sns.barplot(x="období", y="pocet_nakazenych", hue='kraj', data=df_normalized)
    ax.set(xlabel='Období', ylabel='Normalizovaný počet nakažených osob')
    ax.tick_params(axis='x', rotation=45)
    
    legend = ax.get_legend()
    legend.set_title('Kraj')

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+"_1.png"))

    # Graph 2: Dead persons for South-Moravian region
    plt.figure()
    ax = sns.barplot(x="období", y="pocet_umrti", hue='kraj', data=df_normalized)
    ax.set(xlabel='Období', ylabel='Normalizovaný počet úmrtí')
    ax.tick_params(axis='x', rotation=45)
    
    legend = ax.get_legend()
    legend.set_title('Kraj')

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+"_2.png"))

    # Graph 3: Cured persons for South-Moravian region
    plt.figure()
    ax = sns.barplot(x="období", y="pocet_vylecenych", hue='kraj', data=df_normalized)
    ax.set(xlabel='Období', ylabel='Normalizovaný počet vyléčených osob')
    ax.tick_params(axis='x', rotation=45)
    
    legend = ax.get_legend()
    legend.set_title('Kraj')

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+"_3.png"))

    #TODO Graph 4: Vaccinated persons for South-Moravian region

########################################################
#sns.set(rc = {'figure.figsize':(8,5)})
#main body
utils.delete_dir_content(utils.graphs_dir())

visualizeA1("visualizeA1", path.join(utils.extracted_data_dir(), "selectA1.csv"))
visualizeA2("visualizeA2", path.join(utils.extracted_data_dir(), "selectA2.csv"))
visualizeB("visualizeB", path.join(utils.extracted_data_dir(), "selectB.csv"), path.join(utils.extracted_data_dir(), "selectB_regions.csv"))