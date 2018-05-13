import altair as alt
import pandas as pd
import urllib
import json

def loadData():

    url = 'https://raw.githubusercontent.com/hvo/datasets/master/nyc_restaurants_by_cuisine.json'
    response = urllib.request.urlopen(url)
    data = json.load(response)

    df = pd.DataFrame()
    for i in range(len(data)):
        perZip1 = data[i]["perZip"]
        df1 = pd.DataFrame(list(perZip1.items()),columns = ["postcode",data[i]["cuisine"]])
        df1.set_index("postcode",inplace = True)
        df = pd.concat([df,df1],axis = 1)

    df.fillna(0,inplace = True)
    df = df.transpose()
    df.reset_index(inplace = True)
    df.rename(index=str, columns={"index": "cuisine"},inplace = True)
    
    return df

def showRatingDistribution(df, name=''):
    zips = name
    
    try:
        data = df.sort_values(by = zips,ascending=False).head(15)
    except KeyError:
        return alt.Chart(pd.DataFrame()).mark_bar()
    else:

	    color_expression    = "highlight._vgsid_==datum._vgsid_"
	    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "SteelBlue")

	    ## There are two types of selection in our chart:
	    ## (1) A selection for highlighting a bar when the mouse is hovering over
	    highlight_selection = alt.selection_single(name="highlight", empty="all", on="mouseover")

	    ## (2) A selection for updating the rating distribution when the mouse is clicked
	    ## Note the encodings=['y'] parameter is needed to specify that once a selection
	    ## is triggered, it will propagate the encoding channel 'y' as a condition for
	    ## any subsequent filter done on this selection. In short, it means use the data
	    ## field associated with the 'y' axis as a potential filter condition.
	    # rating_selection    = alt.selection_single(name="rating", empty="all", encodings=['y'])

	    ## We need to compute the max count to scale our distribution appropriately
	#    maxCount            = int(data[zips].max())

	    ## Our visualization consists of two bar charts placed side by side. The first one
	    ## sorts the apps by their average ratings as below. Note the compound selection
	    ## that is constructed by adding the two selections together.
	    barMean = alt.Chart(data) \
	        .mark_bar(stroke="Black") \
	        .encode(
	            alt.X(zips+":Q", axis=alt.Axis(title="Restuarants")),
	            alt.Y('cuisine:O', axis=alt.Axis(title="Cuisine".format(name)), 
	                  sort=alt.SortField(field=zips, op="max", order='descending')),
	            alt.ColorValue("LightGrey", condition=color_condition),
	        ).properties(
	            selection = highlight_selection
	        )

	    return barMean
