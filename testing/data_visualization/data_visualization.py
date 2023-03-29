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
    if city == "Dayton":
        del city_traces[4]
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
        divisor = window_max(data_window) - window_min(data_window)
        if divisor == 0:
            # print("[ERROR] Cannot standardize an invalid data window: %s" % data_window)
            divisor = 1
        tmp_window.append((data_window[n] - window_min(data_window)) / divisor)
    return tmp_window


# extract_features returns the features of an instance. A 11x7 array of features.
def extract_features(data_instance_windows):
    instance_features = []
    # This is the incorrect place to min-max-standardize
    # standardized_windows = []
    # count = 0
    # for window in data_instance_windows:
        # print("Window %d: %s" % (count, window))
    #    this_std_window = min_max_standardize(window)
    #    standardized_windows.append(this_std_window)
    #    count = count + 1
    for n in range(len(data_instance_windows)):
        these_features = [window_max(data_instance_windows[n]),
                          window_min(data_instance_windows[n]),
                          window_mean(data_instance_windows[n]),
                          window_variance(data_instance_windows[n]),
                          window_root_mean_square(data_instance_windows[n]),
                          window_skew(data_instance_windows[n]),
                          window_kurtosis(data_instance_windows[n])]
        instance_features.append(these_features)
    print("instance_features: %s" % instance_features)
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


def visualize_one_city_features(city_features):
    # ["max", "min", "mean", "variance", "rms", "skew", "kurtosis"]
    projection = project_features(city_features)
    print("Projections: \n%s" % projection)
    fig = px.scatter(
        projection, x=0, y=1
    )
    fig.show()


# visualize_many_city_features takes an array of multiple cities' features
def visualize_many_city_features(these_city_features):
    # print(these_city_features)
    fig = plotly.Figure()
    fig.update_layout(title_text="Multiple City Features")
    for this_city in these_city_features:
        for these_features in this_city:
            fig.add_trace(plotly.Scatter(project_features(these_features)))
    fig.show()


def project_features(instance_features):
    combined_features = combine_feature_vectors(instance_features)
    df = pd.DataFrame(data=combined_features)
    transposed = df.transpose()
    tsne = TSNE(n_components=1, random_state=0, perplexity=3)
    projections = tsne.fit_transform(transposed.loc[:, :])
    return projections


def project_city_features(city_features):
    combined_features = {}
    for instance in range(len(city_features)):
        this_key = "Instance " + str(instance)
        combined_features[this_key] = combine_feature_vectors(city_features[instance])
    df = pd.DataFrame(data=combined_features)
    transposed = df.transpose()
    # print("Transposed:\n%s" % transposed)
    tsne = TSNE(n_components=2, random_state=0, perplexity=3)
    projections = tsne.fit_transform(transposed.loc[:, :])
    # print(projections)
    x_y_projections = [[], []]
    for m in range(len(projections)):
        x_y_projections[0].append(projections[m][0])
        x_y_projections[1].append(projections[m][1])
    return x_y_projections


def combine_feature_vectors(instance_features):
    np_arrays = ()
    for server_features in instance_features:
        std_features = min_max_standardize(server_features)
        np_arrays = np_arrays + (np.array(std_features),)
    return np.concatenate(np_arrays)


# main

visualize_city_data("Columbus", link_state_info)
# visualize_instance_data("Columbus", link_state_info)
# visualize_instance_data("Liberty Township", link_state_info)
# visualize_instance_data("Framingham", link_state_info)

# print("Their table: ")
# print(px.data.iris())
# city_traces[traces][server][datapoints]
columbus_traces = get_city_traces("Columbus", link_state_info)
dayton_traces = get_city_traces("Dayton", link_state_info)
# liberty_traces = get_city_traces("Liberty Township", link_state_info)
# framingham_traces = get_city_traces("Framingham", link_state_info)

# city_features[instance][features][max, min, mean, variance, rms, skew, kurtosis]
columbus_features = traces_to_features(columbus_traces)
dayton_features = traces_to_features(dayton_traces)
# liberty_features = traces_to_features(liberty_traces)
# framingham_features = traces_to_features(framingham_traces)

# print("Columbus Features:")
# print(columbus_features)
# visualize_one_city_features(columbus_features)
# visualize_many_city_features([columbus_features, dayton_features])

these_city_features = [columbus_features, dayton_features]
cities = ["Columbus", "Dayton"]
fig = plotly.Figure()
fig.update_layout(title_text="Multiple City Features")
for this_city in range(len(these_city_features)):
    x_y_projections = project_city_features(these_city_features[this_city])
    fig.add_trace(plotly.Scatter(x=x_y_projections[0], y=x_y_projections[1], name=cities[this_city], mode="markers"))
fig.show()





client.close()  # disconnect from mongodb
