# Nathan Joslin
# Honors Thesis: Mitigation of JavaScript-Based Fingerprinting Attacks Reliant 
#                on Client Data Generation
# Sprint 2023
# KNN ML Model
# Followed Tutorial: https://www.digitalocean.com/community/tutorials/k-nearest-neighbors-knn-in-python

# NOTES:
#   - Instance: An instance is and instance of data collection, i.e. a user visiting the collection site for 2 min.
#   - Do not call multiple graphing functions at once, as they refer to the same figures. Please download them
#     before graphing another set.


from pymongo import MongoClient
import plotly.graph_objects as plotly
import statistics as stat
import math as math
from scipy.stats import skew
from scipy.stats import kurtosis
import numpy as np
from pymongo.server_api import ServerApi
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# NOTE TO SELF: mongodb queries are case sensitive!

# Global Vars
window_start = 25
window_end = 51
window_size = (window_end - 1) - window_start


# connect to the database
client = MongoClient(
    "mongodb+srv://joslinn1:3Dd4AdJq7briU3TV@pinglocdata.dsgop.mongodb.net/?retryWrites=true&w=majority")
db = client.PingLocDatabase

# retrieve collection
link_state_info = db.UserLinkStateInformation


# functions

# fetch_city_data queries the database and returns all user data collection instances for given city as an array.
def fetch_city_data(city, collection):
    these_docs = []
    for doc in collection.find({"city": city}, {"_id": 0, "city": 1, "linkData": 1}):
        these_docs.append(doc)
    return clean_data(these_docs)


# process_city_data returns an array of all instance traces for a city. [instance][server][datapoints]
def process_city_data(city, collection):
    city_instance_traces = []
    city_data = fetch_city_data(city, collection)
    for data_instance in city_data:
        city_instance_traces.append(reconstruct_trace(data_instance))
    # print("Processed data for city: %s" % city)
    # print("Instances: %d" % len(city_instance_traces))
    # print("Servers: %d" % len(city_instance_traces[0]))
    # print("Datapoints: %d" % len(city_instance_traces[0][5]))
    # print("This Datapoint: %d" % city_instance_traces[1][7][95])
    return city_instance_traces


# parse_data_instance returns a tuple of the city and link data for an instance of data.
def parse_data_instance(data_instance):
    return data_instance.get('city'), data_instance.get('linkData')


# clean_data removes the empty data point present in all data instances
def clean_data(data_array):
    # remove the empty datapoint present in all data instances
    for n in range(len(data_array)):
        data_array[n]['linkData'] = data_array[n].get('linkData')[1:]
    return data_array


# reconstruct_trace scans through all collected data points for an instance of data, returning an array of data traces.
# reconstruct_trace also calls data_string_to_int() to convert the data to arrays of ints.
# Param: string[[serv0(1), ..., serv10(1)], ..., [serv0(n), ..., serv10(n)]]
# Return: int[[serv0(1), ..., serv0(n)], ..., [serv10(1), ..., serv10(n)]]
def reconstruct_trace(data_instance):
    # an array where all pings to each server are arranged together, i.e. [stanford, oregon, etc.]
    organized_data = [[], [], [], [], [], [], [], [], [], [], []]

    # process each collected datapoint in the window of data: datapoint = [serv0, ..., serv10]
    this_data = data_instance.get('linkData')
    for data_point in this_data:
        # append each server's ping to its respective location in organized_data
        for n in range(11):
            organized_data[n].append(data_point[n])
    # convert data as string -> int
    for n in range(11):
        organized_data[n] = data_string_to_int(organized_data[n])
    return organized_data


# data_string_to_int takes a string array of data, returning an int array of data, i.e. a trace
def data_string_to_int(data_trace):
    result = [0] * len(data_trace)
    for n in range(len(data_trace)):
        result[n] = int(data_trace[n])
    return result


# visualize_city_data generates a graph for each server, with traces for each instance of data from the city.
def visualize_city_data(city, collection):
    # initialize graphs
    stanford = plotly.Figure(data=[plotly.Scatter(mode='lines')])
    stanford.update_layout(
        title=city + " -> Stanford",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'     # middle gray
        )
    )
    oregon = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    oregon.update_layout(
        title=city + " -> Oregon State",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    auburn = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    auburn.update_layout(
        title=city + " -> Auburn",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    alaska = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    alaska.update_layout(
        title=city + " -> Alaska",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    texas = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    texas.update_layout(
        title=city + " -> Texas",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    penn_state = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    penn_state.update_layout(
        title=city + " -> Penn State",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    north_dakota = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    north_dakota.update_layout(
        title=city + " -> North Dakota",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    colorado = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    colorado.update_layout(
        title=city + " -> Colorado",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    maine = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    maine.update_layout(
        title=city + " -> Maine",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    wisconsin = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    wisconsin.update_layout(
        title=city + " -> Wisconsin",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )
    florida = plotly.Figure(data=[plotly.Scatter(mode='lines', )])
    florida.update_layout(
        title=city + " -> Florida",
        xaxis_title="Pings",
        yaxis_title="Time Delay(ms)",
        legend_title="Instances",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color='#7f7f7f'  # middle gray
        )
    )

    # get all traces of data from the City
    instance_traces = process_city_data(city, collection)  # city_traces[traces][server][datapoints]
    instance_count = len(instance_traces)

    # build the graphs, one iteration per instance
    for instance in range(instance_count):
        stanford.add_trace(plotly.Scatter(y=instance_traces[instance][0], name=str(instance)))
        oregon.add_trace(plotly.Scatter(y=instance_traces[instance][1], name=str(instance)))
        auburn.add_trace(plotly.Scatter(y=instance_traces[instance][2], name=str(instance)))
        alaska.add_trace(plotly.Scatter(y=instance_traces[instance][3], name=str(instance)))
        texas.add_trace(plotly.Scatter(y=instance_traces[instance][4], name=str(instance)))
        penn_state.add_trace(plotly.Scatter(y=instance_traces[instance][5], name=str(instance)))
        north_dakota.add_trace(plotly.Scatter(y=instance_traces[instance][6], name=str(instance)))
        colorado.add_trace(plotly.Scatter(y=instance_traces[instance][7], name=str(instance)))
        maine.add_trace(plotly.Scatter(y=instance_traces[instance][8], name=str(instance)))
        wisconsin.add_trace(plotly.Scatter(y=instance_traces[instance][9], name=str(instance)))
        florida.add_trace(plotly.Scatter(y=instance_traces[instance][10], name=str(instance)))

    # display the graphs (opens 11 webpages, each with 1 graph)
    stanford.show()
    oregon.show()
    auburn.show()
    alaska.show()
    texas.show()
    penn_state.show()
    north_dakota.show()
    colorado.show()
    maine.show()
    wisconsin.show()
    florida.show()


# visualize_instance_data generates a graph for each instance of data from a city, with traces for each server.
def visualize_instance_data(city, collection):
    # get all traces of data from the City
    instance_traces = process_city_data(city, collection)  # city_traces[traces][server][datapoints]
    for instance in range(len(instance_traces)):
        # initialize graphs
        this_graph = plotly.Figure(data=[plotly.Scatter(mode='lines')])
        this_graph.update_layout(
            title="Instance: " + str(instance),
            xaxis_title="Pings",
            yaxis_title="Time Delay(ms)",
            legend_title="Servers",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color='#7f7f7f'  # middle gray
            )
        )
        for n in range(11):
            university = int_to_university(n)
            this_graph.add_trace(plotly.Scatter(y=instance_traces[instance][n], name="Server: " + university))
        this_graph.show()


def int_to_university(n):
    this_server = "nil"
    match n:
        case 0:
            this_server = "Stanford"
        case 1:
            this_server = "Oregon State"
        case 2:
            this_server = "Auburn"
        case 3:
            this_server = "Alaska"
        case 4:
            this_server = "Texas"
        case 5:
            this_server = "Penn State"
        case 6:
            this_server = "North Dakota"
        case 7:
            this_server = "Colorado"
        case 8:
            this_server = "Maine"
        case 9:
            this_server = "Wisconsin"
        case 10:
            this_server = "Florida"
    return this_server


# parse_instance_windows returns the windows of data for each server of an instance.
def parse_instance_windows(data_instance):
    result = []
    for n in range(11):
        result.append(data_instance[n][window_start:window_end])
    return result


# window_max returns an array of the max values within the given window, for each server of an instance.
def window_max(data_instance_window):
    return max(data_instance_window)


# window_min returns an array of the min values within the given window, for each server of an instance.
def window_min(data_instance_window):
    return min(data_instance_window)


# window_mean returns an array of the sum of values of a window, for each server of an instance.
def window_mean(data_instance_window):
    return sum(data_instance_window) / window_size


# window_variance returns an array of the variances of each server's window in an instance.
def window_variance(data_instance_window):
    return stat.variance(data_instance_window)      # TODO: Not sure if this calculates variance same as paper


# root_mean_square returns the RMS of the window. This reflects the noise of the data window.
def window_root_mean_square(data_instance_window):
    tmp_window = data_instance_window[:]
    for n in range(tmp_window):
        tmp_window[n] = tmp_window[n]**2
    return math.sqrt(sum(tmp_window) / window_size)


# window_skew returns the skew of the window.
def window_skew(data_instance_window):
    return skew(data_instance_window)


# window_kurtosis returns the kurtosis of the window        # TODO: Not sure if calculating right
def window_kurtosis(data_instance_window):
    return kurtosis(data_instance_window)


# min_max_standardize returns the min-max standardization of the window such that all data falls between [0,1]
def min_max_standardize(data_instance_window):
    tmp_window = data_instance_window[:]
    for n in range(tmp_window):
        tmp_window[n] = (data_instance_window[n] - window_min(data_instance_window)) \
                        / (window_max(data_instance_window) - window_min(data_instance_window))
    return tmp_window


def extract_features(data_instance_window):
    standardized_window = min_max_standardize(data_instance_window)
    features = [window_max(standardized_window),
                window_min(standardized_window),
                window_mean(standardized_window),
                window_variance(standardized_window),
                window_root_mean_square(standardized_window),
                window_skew(standardized_window),
                window_kurtosis(standardized_window)]
    return features


# main
visualize_city_data("Columbus", link_state_info)
visualize_instance_data("Columbus", link_state_info)

client.close()  # disconnect from mongodb
