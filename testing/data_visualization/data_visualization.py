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
import plotly.express as px
import statistics as stat
import math as math
from scipy.stats import skew
from scipy.stats import kurtosis
import pandas as pd
from sklearn.manifold import TSNE

import numpy as np
from pymongo.server_api import ServerApi
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# NOTE TO SELF: mongodb queries are case sensitive!

pd.options.plotting.backend = "plotly"

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


# get_city_traces returns an array of all instance traces for a city. [instance][server][datapoints]
def get_city_traces(city, collection):
    city_traces = []
    city_data = fetch_city_data(city, collection)
    for data_instance in city_data:
        city_traces.append(reconstruct_trace(data_instance))
    return city_traces


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
    # get all traces of data from the City
    instance_traces = get_city_traces(city, collection)  # city_traces[traces][server][datapoints]

    for server in range(11):
        server_name = int_to_university(server)
        # initialize server graph
        this_graph = plotly.Figure(data=[plotly.Scatter(mode='lines')])
        this_graph.update_layout(
            title=city + " -> " + server_name,
            xaxis_title="Pings",
            yaxis_title="Time Delay(ms)",
            legend_title="Instances",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color='#7f7f7f'  # middle gray
            )
        )
        # add each instance's trace to this server graph
        for instance in range(len(instance_traces)):
            this_graph.add_trace(plotly.Scatter(y=instance_traces[instance][server], name=str(instance)))
        this_graph.show()


# visualize_instance_data generates a graph for each instance of data from a city, with traces for each server.
def visualize_instance_data(city, collection):
    # get all traces of data from the City
    instance_traces = get_city_traces(city, collection)  # city_traces[traces][server][datapoints]
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


# parse_windows returns the windows of data for each server of an instance.
def parse_windows(trace):
    result = []
    for n in range(11):
        result.append(trace[n][window_start:window_end])
    return result


# window_max returns an array of the max values within the given window, for each server of an instance.
def window_max(data_window):
    return max(data_window)


# window_min returns an array of the min values within the given window, for each server of an instance.
def window_min(data_window):
    return min(data_window)


# window_mean returns an array of the sum of values of a window, for each server of an instance.
def window_mean(data_window):
    return sum(data_window) / window_size


# window_variance returns an array of the variances of each server's window in an instance.
def window_variance(data_window):
    return stat.variance(data_window)  # TODO: Not sure if this calculates variance same as paper


# root_mean_square returns the RMS of the window. This reflects the noise of the data window.
def window_root_mean_square(data_window):
    tmp_window = data_window[:]
    for n in range(len(tmp_window)):
        tmp_window[n] = tmp_window[n] ** 2
    return math.sqrt(sum(tmp_window) / window_size)


# window_skew returns the skew of the window.
def window_skew(data_window):
    return skew(data_window)


# window_kurtosis returns the kurtosis of the window        # TODO: Not sure if calculating right
def window_kurtosis(data_window):
    return kurtosis(data_window)


# min_max_standardize returns the min-max standardization of the window such that all data falls between [0,1]
def min_max_standardize(data_window):
    tmp_window = []
    for n in range(len(data_window)):
        tmp_window.append(
            (data_window[n] - window_min(data_window)) / (window_max(data_window) - window_min(data_window)))
    return tmp_window


# extract_features returns the features of an instance. A 11x7 array of features.
def extract_features(data_instance_windows):
    instance_features = []
    standardized_windows = []
    for window in data_instance_windows:
        min_max_standardize(window)
        standardized_windows.append(window)
    for window in standardized_windows:
        these_features = [window_max(window),
                          window_min(window),
                          window_mean(window),
                          window_variance(window),
                          window_root_mean_square(window),
                          window_skew(window),
                          window_kurtosis(window)]
        instance_features.append(these_features)
    # print("instance_features: %s" % instance_features)
    return instance_features


# traces_to_features converts an array of traces to an array of features.
def traces_to_features(traces):
    instance_windows = []
    for trace in traces:
        instance_windows.append(parse_windows(trace))
    instance_features = []
    for instance in instance_windows:
        instance_features.append(extract_features(instance))
    return instance_features


def visualize_features(city_features):
    # print(len(city_features[0]))
    # features_dict = {}
    # for instance in range(len(city_features)):
    #    features_dict[str(instance)] = city_features[instance]

    # ["max", "min", "mean", "variance", "rms", "skew", "kurtosis"]
    df = pd.DataFrame(data=city_features,
                      index=list('012345'),
                      columns=["Stanford", "Oregon", "Auburn", "Alaska", "Texas", "Penn State", "North Dakota", "Colorado", "Maine", "Wisconsin", "Florida"])
    print("%s" % df)
    # fig = px.scatter_matrix(df)
    # fig.show()
    tsne = TSNE(n_components=2, perplexity=3)
    projections = tsne.fit_transform(df)
    fig = px.scatter(
        projections, x=0, y=1
    )
    fig.show()


# main
# visualize_city_data("Columbus", link_state_info)
# visualize_instance_data("Columbus", link_state_info)

# city_traces[traces][server][datapoints]
# columbus_traces = get_city_traces("Columbus", link_state_info)
# print("Columbus Traces Retrieved: %d" % len(columbus_traces))
# dayton_traces = get_city_traces("Dayton", link_state_info)
# liberty_traces = get_city_traces("Liberty Township", link_state_info)

# city_features[instance][features][max, min, mean, variance, rms, skew, kurtosis]
# columbus_features = traces_to_features(columbus_traces)
# dayton_features = traces_to_features(dayton_traces)
# liberty_features = traces_to_features(liberty_traces)

# print("Columbus Features:")
# print(columbus_features)
# visualize_features(columbus_features)

client.close()  # disconnect from mongodb
