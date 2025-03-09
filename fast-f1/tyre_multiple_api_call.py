from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

race_names = ["Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix" , "Azerbaijan Grand Prix" , "Miami Grand Prix", "Monaco Grand Prix", "Spanish Grand Prix",       
               "Canadian Grand Prix", "British Grand Prix", "Austrian Grand Prix", "Hungarian Grand Prix", "Belgian Grand Prix", "Dutch Grand Prix", "Italian Grand Prix", "Japanese Grand Prix",
               "Qatar Grand Prix", "United States Grand Prix", "Mexico City Grand Prix", "Sao Paulo Grand Prix", "Las Vegas Grand Prix", "Abu Dhabi Grand Prix"]  # Example races
year = 2023  # Modify if needed

for race_name in race_names:
    # Load session for each race
    session = fastf1.get_session(year, race_name, 'R')
    session.load()
    
    # Get laps and stints data
    laps = session.laps
    drivers = session.drivers
    drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]

    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
    stints = stints.rename(columns={"LapNumber": "StintLength"})

    # Create a new figure for each race
    fig, ax = plt.subplots(figsize=(6, 5))

    for driver in drivers:
        driver_stints = stints.loc[stints["Driver"] == driver]
        previous_stint_end = 0

        for _, row in driver_stints.iterrows():
            compound_color = fastf1.plotting.get_compound_color(row["Compound"], session=session)  # FIXED
            ax.barh(
                y=driver,
                width=row["StintLength"],
                left=previous_stint_end,
                color=compound_color,
                edgecolor="black",
                fill=True
            )
            previous_stint_end += row["StintLength"]

    # Formatting
    ax.set_title(f"{race_name} - Tyre Stints")
    ax.set_xlabel("Lap Number")
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    ##plt.show()
    ##plt.draw()
    plt.savefig(f"{race_name.replace(' ', '_')}.png")  # Save each race as an image
    plt.close(fig)  # Close figure to avoid memory issues

print("Plots saved successfully!")
