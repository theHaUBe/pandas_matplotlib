#HUBERT GÓRECKI nr albumu 147599

import pandas as pd
import os
import matplotlib.pyplot as plt
import sqlite3

# 1. Wczytaj dane ze wszystkich plików do pojedynczej tablicy (używając Pandas) --------------------------------------
folder_path = "data/names"
data_frames = []

for file_name in os.listdir(folder_path):
    if file_name.startswith("yob") and file_name.endswith(".txt"):
        year = int(file_name[3:7])
        file_path = os.path.join(folder_path, file_name)

        df = pd.read_csv(file_path, header=None, names=["Name", "Gender", "Frequency"])
        df["Year"] = year
        data_frames.append(df)

all_data = pd.concat(data_frames, ignore_index=True)


# 2. Określi ile różnych (unikalnych) imion zostało nadanych w tym czasie --------------------------------------------
unique_names_total = all_data["Name"].nunique()
print("-------------- Zadanie 2 --------------")
print(f"Liczba unikalnych imion: {unique_names_total}")


# 3. Określić ile różnych (unikalnych) imion zostało nadanych w tym czasie rozróżniając imiona męskie i żeńskie ------
unique_names_by_gender = all_data.groupby("Gender")["Name"].nunique()
print("\n-------------- Zadanie 3 --------------")
print("Liczba unikalnych imion według płci:")
print(unique_names_by_gender.to_string(header=False))


# 4. Stwórz nowe kolumny frequency_male i frequency_female -----------------------------------------------------------
total_births_by_year_gender = all_data.groupby(["Year", "Gender"])["Frequency"].sum().reset_index()
all_data = all_data.merge(total_births_by_year_gender, on=["Year", "Gender"], suffixes=("", "_Total"))
all_data["Popularity"] = all_data["Frequency"] / all_data["Frequency_Total"]

all_data["frequency_male"] = all_data.apply(
    lambda row: row["Popularity"] if row["Gender"] == "M" else 0, axis=1
)
all_data["frequency_female"] = all_data.apply(
    lambda row: row["Popularity"] if row["Gender"] == "F" else 0, axis=1
)


# 5. Wykres liczby narodzin i stosunek płci --------------------------------------------------------------------------
total_births_by_year = all_data.groupby("Year")["Frequency"].sum()
births_by_gender = all_data.groupby(["Year", "Gender"])["Frequency"].sum().unstack()
gender_ratio = births_by_gender["F"] / births_by_gender["M"]

fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

axes[0].plot(total_births_by_year.index, total_births_by_year.values)
axes[0].set_title("Zadanie 5. Całkowita liczba narodzin oraz stosunek płci")
axes[0].set_ylabel("Liczba narodzin")
axes[0].grid(True)

axes[1].plot(gender_ratio.index, gender_ratio.values)
axes[1].set_ylabel("Stosunek narodzin (K/M)")
axes[1].set_xlabel("Rok")
axes[1].grid(True)

plt.tight_layout()
plt.show()

birth_differences = abs(births_by_gender["F"] - births_by_gender["M"])

year_min_diff = birth_differences.idxmin()
year_max_diff = birth_differences.idxmax()

print("\n-------------- Zadanie 5 --------------")
print(f"Najmniejszą różnicę w liczbie urodzin odnotowano w {year_min_diff}")
print(f"Największą różnicę w liczbie urodzin odnotowano w {year_max_diff}")


# 6. Wyznacz 1000 najpopularniejszych imion --------------------------------------------------------------------------
weighted_popularity = all_data.groupby(["Name", "Gender"])["Popularity"].sum().reset_index()
weighted_popularity = weighted_popularity.sort_values(by=["Gender", "Popularity"], ascending=[True, False])

top_1000_male = weighted_popularity[weighted_popularity["Gender"] == "M"].head(1000)
top_1000_female = weighted_popularity[weighted_popularity["Gender"] == "F"].head(1000)


# 7. Wykres popularności ---------------------------------------------------------------------------------------------
john_data = all_data[(all_data["Name"] == "John") & (all_data["Gender"] == "M")]
top_female_name = top_1000_female.iloc[0]["Name"]
top_female_data = all_data[(all_data["Name"] == top_female_name) & (all_data["Gender"] == "F")]

fig, ax1 = plt.subplots(figsize=(14, 8))

ax1.plot(john_data["Year"], john_data["Frequency"], color="blue", label="John - Liczba nadań")
ax1.set_ylabel("Liczba nadań imienia")
ax1.tick_params(axis="y")

ax1.plot(top_female_data["Year"], top_female_data["Frequency"], color="pink", label=f"{top_female_name} - Liczba nadań")

ax2 = ax1.twinx()

ax2.plot(john_data["Year"], john_data["Popularity"], color="green", label="John - Popularność")
ax2.set_ylabel("Popularność imion")
ax2.tick_params(axis="y")

ax2.plot(top_female_data["Year"], top_female_data["Popularity"], color="red", label=f"{top_female_name} - Popularność")

fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9), bbox_transform=ax1.transAxes)
ax1.set_xlabel("Rok")
ax1.set_title(f"Zadanie 7. Najpopularniejsze imiona")
ax1.grid(True)

plt.tight_layout()
plt.show()

selected_years = [1934, 1980, 2022]
john_counts = john_data[john_data["Year"].isin(selected_years)][["Year", "Frequency"]]
female_name_counts = top_female_data[top_female_data["Year"].isin(selected_years)][["Year", "Frequency"]]

print("\n-------------- Zadanie 7 --------------")
print("Imię: John")
print(john_counts.to_string(index=False))

print("\nImię:", top_female_name)
print(female_name_counts.to_string(index=False))


# 8. Procent narodzin dla imion z top1000 ----------------------------------------------------------------------------
top1000_names_male = set(top_1000_male["Name"])
top1000_names_female = set(top_1000_female["Name"])

top1000_data = all_data[
    (all_data["Name"].isin(top1000_names_male) & (all_data["Gender"] == "M")) |
    (all_data["Name"].isin(top1000_names_female) & (all_data["Gender"] == "F"))
]

top1000_births_by_year_gender = top1000_data.groupby(["Year", "Gender"])["Frequency"].sum().unstack()
total_births_by_year_gender = all_data.groupby(["Year", "Gender"])["Frequency"].sum().unstack()
percentage_top1000 = (top1000_births_by_year_gender / total_births_by_year_gender) * 100

fig, ax = plt.subplots(figsize=(14, 8))

ax.plot(percentage_top1000.index, percentage_top1000["M"], label="Mężczyzni", color="blue")
ax.plot(percentage_top1000.index, percentage_top1000["F"], label="Kobiety", color="red")

ax.set_title("\nZadanie 8. Procent imion należących do top1000")
ax.set_xlabel("Rok")
ax.set_ylabel("Procent w top1000 (%)")
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

unique_names_by_year_gender = all_data.groupby(["Year", "Gender"])["Name"].nunique().unstack()
unique_names_diff = abs(unique_names_by_year_gender["M"] - unique_names_by_year_gender["F"])
year_max_diff = unique_names_diff.idxmax()
max_diff_value = unique_names_diff.max()

print("\n-------------- Zadanie 8 --------------")
print(f"Rok z największą różnicą w różnorodności imion: {year_max_diff}")
print("Z biegiem lat coraz więcej osób nosi unikalne imiona. Kobiety od zawsze posiadały, posiadają i zapewne "
      "będą posiadać więcej unikalnych imion od mężczyzn.")


# 9. Hipoteza ostatnich liter imion męskich -------------------------------------------------------------------------
all_data["Last_Letter"] = all_data["Name"].str[-1]
births_by_letter = (
    all_data.groupby(["Year", "Gender", "Last_Letter"])["Frequency"].sum().reset_index()
)

years_to_analyze = [1910, 1970, 2023]
male_data = births_by_letter[(births_by_letter["Gender"] == "M") & (births_by_letter["Year"].isin(years_to_analyze))]

total_births_by_year = all_data[all_data["Gender"] == "M"].groupby("Year")["Frequency"].sum()
male_data = male_data.merge(total_births_by_year, on="Year", suffixes=("", "_Total"))
male_data["Normalized_Frequency"] = male_data["Frequency"] / male_data["Frequency_Total"]

male_pivot = male_data.pivot(index="Last_Letter", columns="Year", values="Normalized_Frequency").fillna(0)

ax = male_pivot.plot(kind="bar", figsize=(14, 8))
ax.set_title("Zadanie 9. Rozkład ostatnich liter imion męskich w wybranych latach")
ax.set_xlabel("Ostatnia litera")
ax.set_ylabel("Procent całkowitej liczby urodzeń")
ax.legend()
ax.grid(axis="y")
ax.set_axisbelow(True)
plt.tight_layout()
plt.show()

change_over_time = male_pivot.max(axis=1) - male_pivot.min(axis=1)
top_3_letters = change_over_time.nlargest(3).index

trend_data = births_by_letter[
    (births_by_letter["Gender"] == "M") & (births_by_letter["Last_Letter"].isin(top_3_letters))
]
trend_data = trend_data.merge(total_births_by_year, on="Year", suffixes=("", "_Total"))
trend_data["Normalized_Frequency"] = trend_data["Frequency"] / trend_data["Frequency_Total"]

fig, ax = plt.subplots(figsize=(14, 8))
for letter in top_3_letters:
    letter_trend = trend_data[trend_data["Last_Letter"] == letter]
    ax.plot(letter_trend["Year"], letter_trend["Normalized_Frequency"], label=f"Litera '{letter}'")

ax.set_title("Zadanie 9b. Trend popularności 3 liter z największą zmianą w czasie")
ax.set_xlabel("Rok")
ax.set_ylabel("Procent całkowitej liczby urodzeń")
ax.legend()
ax.grid(axis="y")
ax.set_axisbelow(True)
plt.tight_layout()
plt.show()

change_1910_2023 = male_pivot[2023] - male_pivot[1910]
max_increase_letter = change_1910_2023.idxmax()
max_increase_value = change_1910_2023.max()
max_decrease_letter = change_1910_2023.idxmin()
max_decrease_value = change_1910_2023.min()

print("-------------- Zadanie 9 --------------")
print("Prawdą jest, że w obserwowanym okresie rozkład ostatnich liter imion męskich uległ istotnej zmianie.")
print(f"Największy wzrost popularności: Litera '{max_increase_letter}', wzrost o {max_increase_value:.4f}")
print(f"Największy spadek popularności: Litera '{max_decrease_letter}', spadek o {max_decrease_value:.4f}")


# 10. Imiona nadawane obu płciom i analiza zmiany konotacji ----------------------------------------------------------
gender_counts = all_data.groupby(["Name", "Gender"])["Frequency"].sum().unstack(fill_value=0)
gender_counts = gender_counts[(gender_counts["M"] > 0) & (gender_counts["F"] > 0)]
unisex_names = gender_counts.index

time_periods = {
    "before_1920": (1880, 1920),
    "after_2000": (2000, 2022),
}

proportions = {}
for period, (start_year, end_year) in time_periods.items():
    period_data = all_data[(all_data["Year"] >= start_year) & (all_data["Year"] <= end_year)]
    name_gender_totals = period_data.groupby(["Name", "Gender"])["Frequency"].sum().unstack(fill_value=0)
    name_totals = name_gender_totals.sum(axis=1)
    proportions[period] = name_gender_totals.div(name_totals, axis=0)

changes = {}
for name in unisex_names:
    p_m_before = proportions["before_1920"].loc[name, "M"] if name in proportions["before_1920"].index else 0
    p_f_after = proportions["after_2000"].loc[name, "F"] if name in proportions["after_2000"].index else 0
    p_f_before = proportions["before_1920"].loc[name, "F"] if name in proportions["before_1920"].index else 0
    p_m_after = proportions["after_2000"].loc[name, "M"] if name in proportions["after_2000"].index else 0

    change_m_to_f = (p_m_before + p_f_after) / 2
    change_f_to_m = (p_f_before + p_m_after) / 2

    if 0 < change_m_to_f < 1 or 0 < change_f_to_m < 1:
        changes[name] = {"m_to_f": change_m_to_f, "f_to_m": change_f_to_m}

changes_df = pd.DataFrame(changes).T
changes_df = changes_df.sort_values(by=["m_to_f", "f_to_m"], ascending=[False, False])

top_m_to_f = changes_df["m_to_f"].idxmax()
top_f_to_m = changes_df["f_to_m"].idxmax()

print("\n-------------- Zadanie 10 --------------")
print(f"Imię, z męskiego na żeńskie: {top_m_to_f}")
print(f"Imię, z żeńskiego na męskie: {top_f_to_m}")

fig, ax = plt.subplots(2, 1, figsize=(14, 8))

for idx, name in enumerate([top_m_to_f, top_f_to_m]):
    name_data = all_data[all_data["Name"] == name].groupby(["Year", "Gender"])["Frequency"].sum().unstack(fill_value=0)
    name_totals = name_data.sum(axis=1)
    name_proportions = name_data.div(name_totals, axis=0)

    ax[idx].plot(name_proportions.index, name_proportions["M"], label="Mężczyźni", color="blue")
    ax[idx].plot(name_proportions.index, name_proportions["F"], label="Kobiety", color="pink")

    ax[idx].set_title(f"Zadanie 10. Trend popularności imienia '{name}'")
    ax[idx].set_xlabel("Rok")
    ax[idx].set_ylabel("Proporcja nadań")
    ax[idx].legend()
    ax[idx].grid(True)

plt.tight_layout()
plt.show()

###################################################################################################################
db_path = 'data/names_pl_2000-23.sqlite'

conn = sqlite3.connect(db_path)
query = """
SELECT Rok, Imię, Płeć, SUM(Liczba) AS Liczba
FROM (
    SELECT * FROM females
    UNION ALL
    SELECT * FROM males
)
GROUP BY Rok, Imię, Płeć;
"""
data = pd.read_sql_query(query, conn)
conn.close()

# Zadanie 2: Top 200 imion + ostatnia litera -------------------------------------------------------------------------
data['Last_Letter'] = data['Imię'].str[-1]
total_births_per_year = data.groupby('Rok')['Liczba'].sum()
data['Normalized'] = data['Liczba'] / data['Rok'].map(total_births_per_year)

top_200_names = (
    data.groupby('Imię')['Normalized']
    .sum()
    .sort_values(ascending=False)
    .head(200)
)

letter_trends = (
    data.groupby(['Rok', 'Płeć', 'Last_Letter'])['Liczba']
    .sum()
    .reset_index()
)

years_to_compare = [2000, 2013, 2023]
men_letters = letter_trends[letter_trends['Płeć'] == 'M']
selected_years_data = men_letters[men_letters['Rok'].isin(years_to_compare)]

total_births_per_year = men_letters.groupby('Rok')['Liczba'].sum()
selected_years_data = selected_years_data.copy()
selected_years_data['Normalized'] = selected_years_data['Liczba'] / selected_years_data['Rok'].map(total_births_per_year)

pivot_data = selected_years_data.pivot(index='Last_Letter', columns='Rok', values='Normalized').fillna(0)

pivot_data.plot(kind='bar', figsize=(14, 8))
plt.title("Zadanie 2. Popularność ostatnich liter imion męskich")
plt.xlabel("Ostatnia litera imienia")
plt.ylabel("Znormalizowana popularność")
plt.legend(title="Rok")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

change_2000_2023 = pivot_data[2023] - pivot_data[2000]
top_3_increases = change_2000_2023.nlargest(3).index
top_3_decreases = change_2000_2023.nsmallest(3).index
print("\n-------------- Zadanie 2 --------------")
print("Największe wzrosty: ", top_3_increases.tolist())
print("Największe spadki: ", top_3_decreases.tolist())
print("Zmiany te są porównywalne do tych zaobserowanych w USA. Na przykład litera 'N' jako ostatnia litera imienia "
      "zyskała na przestrzeni lat dużą popularność zrówno w Polsce jak i w USA")

# Zadanie 3: Znalezienie imion stosunkowo często nadawanych dziewczynkom i chłopcom ---------------------------------
common_names = data.groupby(['Imię', 'Płeć'])['Liczba'].sum().unstack(fill_value=0)
common_names['Similarity'] = (
    common_names.min(axis=1) / common_names.max(axis=1)
)
common_names['Weighted_Similarity'] = (
    common_names['Similarity'] * common_names.sum(axis=1)
)
most_common = common_names.sort_values(by='Weighted_Similarity', ascending=False).head(2)

print("\n-------------- Zadanie 3 --------------")
print("Imiona nadawane stosunkowo często dziewczynkom i chłopcom:")
print(most_common)