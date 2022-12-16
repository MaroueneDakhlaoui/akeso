def function1(filepath: str) ->; pd.DataFrame:
    # Read in an Excel file at the given file path, skipping the first row, and store the resulting DataFrame
    daily_thresholds = pd.read_excel(filepath, skiprows=1)

    # If the ";Req Point;" column is not in daily_thresholds, add a new column with this name and set all of its values to nan
    if ";Req Point"; not in daily_thresholds.columns:
        daily_thresholds[";Req Point";] = np.nan
    # If the ";Req Point;" column is already in daily_thresholds, replace the values in the ";Threshold Eaches;" column with 0 wherever the corresponding value in the ";Req Point;" column is ";150129;", and keep the original value otherwise
    else:
        daily_thresholds[";Threshold Eaches";] = np.where(
            daily_thresholds[";Req Point";]==";150129";,
            0, daily_thresholds[";Threshold Eaches";])

    # Create a list of column names
    cols = [";DOH code";, ";Req Point";, ";Trust Type";, ";Category";, ";Threshold Eaches";]

    # Return a new DataFrame with only the columns in cols from daily_thresholds
    return daily_thresholds[cols]
