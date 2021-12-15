from textwrap import wrap
import utils
import os, csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os import path

# A1 - distribution of infected people by age in regions
def visualizeA1(name, csv_path):
    print("- " + name)
    df = pd.read_csv(csv_path)

    plt.figure()
    sns.set_theme(style="darkgrid")
    ax = sns.boxplot(x="vek", y="kraj", data=df)
    ax.set(xlabel='Věk', ylabel='Kraj')
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+".png"))

# A2 - Series of barplots
def visualizeA2(name, csv1_path, csv2_path):
    print("- " + name)
    df_people = pd.read_csv(csv1_path)
    df_regions = pd.read_csv(csv2_path)

    df = df_people.join(df_regions.set_index('kraj_nuts_kod'), on='kraj_nuts_kod')

    # Graph 1: total number of vaccination for each region
    sns.set_theme(style="darkgrid")

    df1 = df.groupby(['kraj_nazev']).count()
    df1 = df1.reset_index()

    plt.figure()
    ax = sns.barplot(x="vekova_skupina", y="kraj_nazev", data=df1)
    ax.set(xlabel='Počet naočkovaných osob', ylabel='Kraj')
    ax.ticklabel_format(style='plain', axis='x')
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+"_1.png"))

    # Graph 2: total number of vaccination for each region divided by sex
    df2 = df.dropna(subset=['pohlavi']) 
    df2 = df2.groupby(['kraj_nazev', 'pohlavi']).count()
    df2 = df2.reset_index()

    plt.figure()
    ax = sns.barplot(x="vekova_skupina", y="kraj_nazev", hue='pohlavi', data=df2)
    ax.set(xlabel='Počet naočkovaných osob', ylabel='Kraj')
    ax.ticklabel_format(style='plain', axis='x')
    ax.tick_params(axis='x', rotation=45)
    
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
    df3 = df3.groupby(['kraj_nazev', 'vekova_skupina']).count()
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
    df3 = df3.groupby(['kraj_nazev', 'skupina']).sum()
    df3 = df3.reset_index()

    plt.figure()
    ax = sns.barplot(x="pohlavi", y="kraj_nazev", hue='skupina', data=df3)
    ax.set(xlabel='Počet naočkovaných osob', ylabel='Kraj')
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
    date_to = utils.get_current_date()
    date_from = utils.get_date_year_ago()
    df_cummulative = df_cummulative.loc[(df_cummulative['datum'] >= date_from) & (df_cummulative['datum'] <= date_to)]
    
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

# D1 - Show number of vaccinations with each vaccine for all age groups 
def visualizeD1(name, csv_path):
    print("- " + name)
    df = pd.read_csv(csv_path)

    # Count for each class
    df['count'] = 'ok'
    df = df.groupby(by=['vekova_skupina', 'vakcina']).count()
    df = df.reset_index()

    # Make COVID-19 Vaccine Janssen name smaller
    df['vakcina'] = ['Janssen' if row['vakcina'] == 'COVID-19 Vaccine Janssen' else row['vakcina'] for index, row in df.iterrows()]

    # Graph
    plt.figure()
    ax = sns.barplot(x="vekova_skupina", y="count", hue='vakcina', data=df)
    ax.set(xlabel='Věková skupina', ylabel='Počet očkování')
    ax.tick_params(axis='x', rotation=45)
    
    legend = ax.get_legend()
    legend.set_title('Vakcína')

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+".png"))

# D2 - Show vaccination influance on new cases in Prague
def visualizeD2(name, csv1_path, csv2_path):
    print("- " + name)
    df_cases = pd.read_csv(csv1_path)
    df_vaccination = pd.read_csv(csv2_path)
    df_vaccination = df_vaccination.sort_values(by=['_id'])
    df_vaccination = df_vaccination.rename(columns={"_id": "datum", "count": "count"})

    # Cut dataframes to match dates
    first_vaccination = df_vaccination['datum'].iloc[0]
    first_case = df_cases['datum'].iloc[0]
    last_vaccination = df_vaccination['datum'].iloc[-1]
    last_case = df_cases['datum'].iloc[-1]

    if first_vaccination < first_case:
        df_vaccination = df_vaccination.drop(df_vaccination[df_vaccination.datum < first_case].index)
    else:
        df_cases = df_cases.drop(df_cases[df_cases.datum < first_vaccination].index)

    if last_vaccination > last_case:
        df_vaccination = df_vaccination.drop(df_vaccination[df_vaccination.datum > last_case].index)
    else:
        df_cases = df_cases.drop(df_cases[df_cases.datum > last_vaccination].index)

    # Create cumulative counts
    df_cases = df_cases.sort_values(by=['datum'])
    df_vaccination = df_vaccination.sort_values(by=['datum'])
    df_cases['kumulativni_pocet'] = df_cases['count'].iloc[0]
    df_vaccination['kumulativni_pocet'] = df_vaccination['count'].iloc[0]

    cumulative_count = list()
    cases_sum = 0
    for index, row in df_cases.iterrows():
        cases_sum += row['count']
        cumulative_count.append(cases_sum)

    df_cases['kumulativni_pocet'] = cumulative_count

    cumulative_count = list()
    cases_sum = 0
    for index, row in df_vaccination.iterrows():
        cases_sum += row['count']
        cumulative_count.append(cases_sum)

    df_vaccination['kumulativni_pocet'] = cumulative_count

    # Group data to months
    df_cases = df_cases.loc[df_cases.datum.str.contains('^\d{4}-\d{2}-01'), :]
    df_vaccination = df_vaccination.loc[df_vaccination.datum.str.contains('^\d{4}-\d{2}-01'), :]

    # Add column for hue
    df_cases['typ'] = 'Nakažení'
    df_vaccination['typ'] = 'Vakcinace'

    df = df_cases.append(df_vaccination, ignore_index=True)
    df = df.sort_values(by=['datum'])

    # Graph
    plt.figure()
    ax = sns.lineplot(x="datum", y="kumulativni_pocet", hue='typ', data=df)
    ax.set(xlabel='Období', ylabel='Kumulativní pocet výskytů')
    ax.tick_params(axis='x', rotation=45)
    
    legend = ax.get_legend()
    legend.set_title('Typ')

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path.join(utils.graphs_dir(), name+".png"))

# C - Data preparation for mining 
def prepareC(name, csv1_path, csv2_path, csv3_path, csv4_path):
    print("- " + name)
    df_cases = pd.read_csv(csv1_path)
    df_vax = pd.read_csv(csv2_path)
    df_pop = pd.read_csv(csv3_path)

    # Keep data from last 12 months
    date_to = utils.get_current_date()
    date_from = utils.get_date_year_ago()
    df_cases = df_cases.loc[(df_cases['datum'] >= date_from) & (df_cases['datum'] <= date_to)]
    df_vax = df_vax.loc[(df_vax['datum'] >= date_from) & (df_vax['datum'] <= date_to)]

    # Get 50 cities
    cities = []
    with open(csv4_path) as file_name:
        file_read = csv.reader(file_name, delimiter=',')
        for city in file_read:
            cities.append(''.join(city))

    # Total number of new cases in 50 cities
    df_cases = df_cases.loc[df_cases['mesto'].isin(cities)]
    df_cases = df_cases.groupby(['mesto']).sum()
    df_cases.columns = ['pocet_nakazenych']

    # Total number of vaccinated in 50 cities
    df_vax = df_vax.loc[df_vax['mesto'].isin(cities)]
    df_vax = df_vax.groupby(['mesto']).count()
    df_vax.columns = ['pocet_ockovanych']

    df_pop = df_pop.replace(to_replace ="Hlavní město Praha", value ="Praha")
    df_pop = df_pop.replace(to_replace ="Plzeň-město", value ="Plzeň")
    df_pop = df_pop.replace(to_replace ="Ostrava-město", value ="Ostrava")
    df_pop = df_pop.replace(to_replace ="Brno-město", value ="Brno")

    # Merge population into 3 groups of each city
    group_1 = ['0-5', '05-10', '10-15']
    df_pop_1 = df_pop.loc[df_pop['vek_txt'].isin(group_1)]
    df_pop_1 = df_pop_1.groupby(['mesto']).sum()
    df_pop_1.columns = ['populace_0-14']
    
    group_2 = ['15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60']
    df_pop_2 = df_pop.loc[df_pop['vek_txt'].isin(group_2)]
    df_pop_2 = df_pop_2.groupby(['mesto']).sum()
    df_pop_2.columns = ['populace_15-59']

    group_3 = ['60-65', '65-70', '70-75', '75-80', '80-85', '85-90', '90-95', '95+']
    df_pop_3 = df_pop.loc[df_pop['vek_txt'].isin(group_3)]
    df_pop_3 = df_pop_3.groupby(['mesto']).sum()
    df_pop_3.columns = ['populace_60+']

    ###### Detect and replace outliers
    q1 = df_cases['pocet_nakazenych'].quantile(q=0.25, interpolation='linear')
    q3 = df_cases['pocet_nakazenych'].quantile(q=0.75, interpolation='linear')
    iqr = q3- q1

    lower_range = q1 - (1.5 * iqr)
    upper_range = q3 + (1.5 * iqr)
    
    # Replace outliers by min and max value
    edited_outliers = list()
    for index, row in df_cases.iterrows():
        if row['pocet_nakazenych'] > upper_range:
            edited_outliers.append([index, round(upper_range)])
        elif row['pocet_nakazenych'] < lower_range:
            edited_outliers.append([index, round(lower_range)])
        else:
            edited_outliers.append([index, row['pocet_nakazenych']])

    df_cases_outliers = pd.DataFrame(edited_outliers, columns=['mesto', 'pocet_nakazenych'])
    df_cases_outliers = df_cases_outliers.rename(columns={"mesto": "mesto", "pocet_nakazenych": "pocet_nakazenych_upravene_odlehle_hodnoty"})
    
    # Normalization (min-max)
    normalized_cases = (df_cases - df_cases.min()) / (df_cases.max() - df_cases.min())
    normalized_cases.columns = ['normalizovany_pocet_nakazenych']

    # Discretization
    n_intervals = 10
    vax = df_vax["pocet_ockovanych"]
    interval_range = (vax.max() - vax.min()) / n_intervals + 1
    interval_from = vax.min() - interval_range
    interval_to = vax.min()
    df_vax_disc = pd.DataFrame()
    for i in range(n_intervals):
        interval_from += interval_range
        interval_to += interval_range
        for city, row in df_vax.iterrows():
            if (int(row['pocet_ockovanych']) > interval_from) and (int(row['pocet_ockovanych']) < interval_to):
                df_vax_disc = df_vax_disc.append({'mesto': city, 'interval_poctu_ockovanych': str(round(interval_from, 1)) + "-" + str(round(interval_to, 1))}, ignore_index=True)


    # Save as csv file
    df = pd.merge(df_cases, normalized_cases, on = 'mesto')
    df = pd.merge(df, df_cases_outliers, on = 'mesto')
    df = pd.merge(df, df_vax, on = 'mesto')
    df = pd.merge(df, df_vax_disc, on = 'mesto')
    df = pd.merge(df, df_pop_1, on = 'mesto')
    df = pd.merge(df, df_pop_2, on = 'mesto')
    df = pd.merge(df, df_pop_3, on = 'mesto')
    df.to_csv(os.path.join(utils.extracted_data_dir(), "selectC_prepared_for_DM.csv"), encoding='utf-8')


########################################################
#main body
utils.delete_dir_content(utils.graphs_dir())

visualizeA1("visualizeA1", path.join(utils.extracted_data_dir(), "selectA1.csv"))
visualizeA2("visualizeA2", path.join(utils.extracted_data_dir(), "selectA2.csv"), path.join(utils.static_data_dir(), "cz_regions.csv"))
visualizeB("visualizeB", path.join(utils.extracted_data_dir(), "selectB.csv"), path.join(utils.extracted_data_dir(), "selectB_regions.csv"))
visualizeD1("visualizeD1", path.join(utils.extracted_data_dir(), "selectD1.csv"))
visualizeD2("visualizeD2", path.join(utils.extracted_data_dir(), "selectD2_new_cases.csv"), path.join(utils.extracted_data_dir(), "selectD2_vaccinated.csv"))
prepareC("prepareC", path.join(utils.extracted_data_dir(), "selectC_new_cases.csv"), path.join(utils.extracted_data_dir(), "selectC_vaccinated.csv"), path.join(utils.extracted_data_dir(), "selectC_population.csv"), path.join(utils.static_data_dir(), "top_50_cities.csv"))

print("Visualization Done")