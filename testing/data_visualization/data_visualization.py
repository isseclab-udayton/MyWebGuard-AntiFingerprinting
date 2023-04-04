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
from sklearn.metrics import accuracy_score

import numpy as np
from pymongo.server_api import ServerApi
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# NOTE TO SELF: mongodb queries are case sensitive!


pd.options.plotting.backend = "plotly"

# Global Vars
# windows are a subset of a data collection instance. the goal here is to wait a warm-up period
# as the network is not as stable initially.
window_start = 20
window_end = 40
window_size = (window_end - 1) - window_start

# connect to the database
client = MongoClient(
    "mongodb+srv://joslinn1:3Dd4AdJq7briU3TV@pinglocdata.dsgop.mongodb.net/?retryWrites=true&w=majority")
db = client.PingLocDatabase

# retrieve collection
link_state_info = db.UserLinkStateInformation


# functions

def fetch_city_data(city, collection):
    '''
    fetch_city_data queries the database and returns all user data collection instances for given city as an array.
    :param city: the city to query for
    :param collection: the collection to query
    :return: every instance of data collection for this city. A 3-D array.
    '''
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
    if city == "Columbus":
        instance_traces = remove_instances(instance_traces, [4])
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
    return np.var(data_window, axis=0, dtype=np.float64)


# a manual calculation of variance
def window_variance2(data_window):
    this_mean = window_mean(data_window)
    tmp_sum = 0
    for ping in data_window:
        tmp_sum += (ping - this_mean)**2
    print("window_variance2: %d  Mean: %d tmp_sum: %d Window: %s" % (tmp_sum / (len(data_window)-1), this_mean, tmp_sum, data_window))
    return tmp_sum / (len(data_window) - 1)


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
    # NOTE: This is the incorrect place to min-max-standardize
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
    # print("instance_features: %s" % instance_features)
    return instance_features


def extract_features2(data_instance_windows):
    '''
    extract_features2 extracts features from windows with pings >800 removed prior to all calculations.
    The important addition in the second version is the addition of a new feature: lost packet count.
    :param data_instance_windows: the instance of windows to calculate features for.
    :return: the 2-D array of features
    '''
    instance_features = []
    for n in range(len(data_instance_windows)):
        lost_packets, new_window = remove_lost_packets(data_instance_windows[n])
        these_features = [window_max(new_window),
                          window_min(new_window),
                          window_mean(new_window),
                          window_variance(new_window),
                          window_root_mean_square(new_window),
                          window_skew(new_window),
                          window_kurtosis(new_window),
                          lost_packets]
        instance_features.append(these_features)
    # print("instance_features from extraction v2: %s\n" % instance_features)
    return instance_features


def extract_features_one(window):
    these_features = [window_max(window),
                      window_min(window),
                      window_mean(window),
                      window_variance(window),
                      window_root_mean_square(window),
                      window_skew(window),
                      window_kurtosis(window)]
    # print("Features: %s" % these_features)
    return these_features


# traces_to_features converts an array of traces to an array of features.
def traces_to_features(traces):
    instance_windows = []
    for trace in traces:
        instance_windows.append(parse_windows(trace))
    instance_features = []
    for instance in instance_windows:
        instance_features.append(extract_features(instance))
    return instance_features


# traces_to_windows converts a 2D array of traces to a 2D array of windows.
def traces_to_windows(traces):
    instance_windows = []
    for trace in traces:
        instance_windows.append(parse_windows(trace))
    return instance_windows


# NOT USED
def windows_to_features(windows):
    '''
    windows_to_features extracts features from all windows of an instance.
    :param windows: the windows of an instance
    :return: the features for each window, a 2-D array
    '''
    window_features = []
    for window in windows:
        print("This window: %s" % window)
        print(window.tolist())
        window_features.append(extract_features(window.tolist()))
    return window_features


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


# project_features uses tsne projections to project the 77-dimensional feature vector into 2-D space.
def project_features(instance_features):
    combined_features = combine_feature_vectors(instance_features)
    df = pd.DataFrame(data=combined_features)
    transposed = df.transpose()
    tsne = TSNE(n_components=1, random_state=0, perplexity=3)
    projections = tsne.fit_transform(transposed.loc[:, :])
    return projections


# project_city_features is similar to project_features except that it can handle multiple instances, thus
# it can project all instances of a city. It returns an x-cord array and a y-cord aray combined into a 2-D array.
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


# combine_feature_vectors combines 11, 7-feature vectors into a single 77-feature vector
def combine_feature_vectors(instance_features):
    np_arrays = ()
    for server_features in instance_features:
        # std_features = min_max_standardize(server_features)
        np_arrays = np_arrays + (np.array(server_features),)
    singe_vector = np.concatenate(np_arrays)
    return min_max_standardize(singe_vector)


def remove_instances(city_instances, remove_me):
    '''
    remove_instances removes a set of indexs from an array of instances.
    :param city_instances: a 3-D array of instances
    :param remove_me: the indexes to remove
    :return: the valid data instances
    '''
    removed_index = 0
    processed = []
    # for each instance
    for n in range(len(city_instances)):
        if n == remove_me[removed_index]:
            if len(remove_me) == removed_index + 1:     # if there's only one index to remove this avoids an error
                return processed
            removed_index += 1
        else:
            processed.append(city_instances[n])
    return processed


# duplicate_with_noise duplicates a set of windows (representing a single instance), with some noise.
def duplicate_with_noise(these_windows, noise):
    dup_instance = []
    # for each server
    for window in these_windows:
        noisy_modifiers = np.random.rand(1, len(window))     # this applies "variance" to our data
        # print("Introducing 0-%dms of noise to synthetic data..." % noise)
        noisy_variance = noise * noisy_modifiers  # window is now float64's
        # print(noisy_variance)
        noisy_window = np.add(window, noisy_variance)
        dup_instance.append(noisy_window[0])  # remove the weird extra outer array
        # print("Synthetic Window   Max: %d Min: %d" % (window_max(noisy_window[0]), window_min(noisy_window[0])))
    return np.rint(dup_instance).astype(int)  # return as integers


def create_synthetic_data(city_name, city_windows, factor, noise):
    '''
    :param city_name: name of the city
    :param city_windows: the windows to base synthetic windows off of
    :param factor: how many synthetic traces per city instance
    :param noise: the noise in milliseconds to introduce to the data
    :return: factor * len(city_windows) number of synthetic traces
    '''
    synthetic_instances = []
    for n in range(factor):
        for instance in city_windows:
            synthetic_instances.append(duplicate_with_noise(instance, noise))
    print("Created %d synthetic traces from %d real traces for the city of %s." % (len(synthetic_instances), len(city_windows), city_name))
    return synthetic_instances


def visualize_windows_by_server(city_name, these_windows):
    '''
    visualize_windows_by_server creates a graph for each server ping, populated with an arbitrary number of instance traces
    :param city_name: the name of the city of which the windows are from
    :param these_windows: the window of pings to visualize, a 3-D array
    :return:
    '''
    for server in range(11):
        server_name = int_to_university(server)
        # initialize server graph
        this_graph = plotly.Figure(data=[plotly.Scatter(mode='lines')])
        this_graph.update_layout(
            title=city_name + " -> " + server_name,
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
        for instance in range(len(these_windows)):
            this_graph.add_trace(plotly.Scatter(y=these_windows[instance][server], name=str(instance)))
        this_graph.show()


def remove_lost_packets(window):
    '''
    remove_lost_packets removes packets with a ping greater than 800.
    :param window: the window from which to remove lost packets
    :return: the count of packets removed, and the resulting window
    '''
    lost_packets = 0
    # print("Old window: %s" % window)
    for n in range(len(window)):
        if window[n] > 800:
            np.delete(window, n)
            lost_packets += 1
    # print("New window: %s" % window)
    return lost_packets, window


# main

# visualize_city_data("Columbus", link_state_info)
# visualize_instance_data("Columbus", link_state_info)
# visualize_instance_data("Liberty Township", link_state_info)
# visualize_instance_data("Framingham", link_state_info)
# visualize_instance_data("Dayton", link_state_info)

# print("Their table: ")
# print(px.data.iris())
# city_traces[traces][server][datapoints]
# columbus_traces = get_city_traces("Columbus", link_state_info)
# dayton_traces = get_city_traces("Dayton", link_state_info)
# liberty_traces = get_city_traces("Liberty Township", link_state_info)
# framingham_traces = get_city_traces("Framingham", link_state_info)

# city_features[instance][features][max, min, mean, variance, rms, skew, kurtosis]
# columbus_features = traces_to_features(columbus_traces)
# dayton_features = traces_to_features(dayton_traces)
# liberty_features = traces_to_features(liberty_traces)
# framingham_features = traces_to_features(framingham_traces)

# print("Columbus Features:")
# print(columbus_features)
# visualize_one_city_features(columbus_features)
# visualize_many_city_features([columbus_features, dayton_features])

# display tsne projection of multiple cities
# these_city_features = [columbus_features, dayton_features]
# cities = ["Columbus", "Dayton"]
# fig = plotly.Figure()
# fig.update_layout(title_text="Multiple City Features")
# for this_city in range(len(these_city_features)):
#     x_y_projections = project_city_features(these_city_features[this_city])
#     fig.add_trace(plotly.Scatter(x=x_y_projections[0], y=x_y_projections[1], name=cities[this_city], mode="markers"))
# fig.show()

NOISE = 50
K_VALUE = 45
NEW_FEATURES = False

# Columbus Synthetic data
columbus_traces_unprocessed = get_city_traces("Columbus", link_state_info)
columbus_traces_processed = remove_instances(columbus_traces_unprocessed, [2, 4])
# visualize_windows_by_server("Columbus", columbus_traces_processed)
columbus_windows = traces_to_windows(columbus_traces_processed)
synthetic_columbus_windows = create_synthetic_data("Columbus", columbus_windows, 30, NOISE)
# visualize_windows_by_server("Columbus", synthetic_columbus_windows)
synthetic_columbus_features = []
for synthetic_instance in synthetic_columbus_windows:
    synthetic_columbus_features.append(extract_features(synthetic_instance))
print("Extracted features from %d instances for the city of %s." % (len(synthetic_columbus_features), "Columbus"))
# Visualize synthetic columbus data     NOTE: visualizing here results in wrong axis label, pings are x1000?
# visualize_windows_by_server("Columbus", synthetic_columbus_windows)

# Dayton synthetic data
# dayton_traces = get_city_traces("Dayton", link_state_info)
# dayton_windows = traces_to_windows(dayton_traces)
# synthetic_dayton_windows = create_synthetic_data("Dayton", dayton_windows, 18, NOISE)
# visualize_windows_by_server("Dayton", synthetic_dayton_windows)
# synthetic_dayton_features = []
# for synthetic_instance in synthetic_dayton_windows:
#     synthetic_dayton_features.append(extract_features(synthetic_instance))
# print("Extracted features from %d instances for the city of %s." % (len(synthetic_dayton_features), "Dayton"))

# Wildwood synthetic data
wildwood_traces = get_city_traces("Wildwood", link_state_info)
wildwood_windows = traces_to_windows(wildwood_traces)
synthetic_wildwood_windows = create_synthetic_data("Wildwood", wildwood_windows, 40, NOISE)
synthetic_wildwood_features = []
for synthetic_instance in synthetic_wildwood_windows:
    synthetic_wildwood_features.append(extract_features(synthetic_instance))
print("Extracted features from %d instances for the city of %s." % (len(synthetic_wildwood_features), "Wildwood"))

# Framingham synthetic data
framingham_traces = get_city_traces("Framingham", link_state_info)
framingham_windows = traces_to_windows(framingham_traces)
synthetic_framingham_windows = create_synthetic_data("Framingham", framingham_windows, 40, NOISE)
synthetic_framingham_features = []
for synthetic_instance in synthetic_framingham_windows:
    synthetic_framingham_features.append(extract_features(synthetic_instance))
print("Extracted features from %d instances for the city of %s." % (len(synthetic_framingham_features), "Framingham"))

# Menomie synthetic data
menomonie_traces = get_city_traces("Menomonie", link_state_info)
menomonie_windows = traces_to_windows(menomonie_traces)
synthetic_menomonie_windows = create_synthetic_data("Menomonie", menomonie_windows, 40, NOISE)
synthetic_menomonie_features = []
for synthetic_instance in synthetic_menomonie_windows:
    synthetic_menomonie_features.append(extract_features(synthetic_instance))
print("Extracted features from %d instances for the city of %s." % (len(synthetic_menomonie_features), "Menomonie"))

# Los Angeles synthetic data
la_traces = get_city_traces("Los Angeles", link_state_info)
la_windows = traces_to_windows(la_traces)
synthetic_la_windows = create_synthetic_data("Los Angeles", la_windows, 40, NOISE)
synthetic_la_features = []
for synthetic_instance in synthetic_la_windows:
    synthetic_la_features.append(extract_features(synthetic_instance))
print("Extracted features from %d instances for the city of %s." % (len(synthetic_la_features), "Los Angeles"))
visualize_windows_by_server("Los Angeles", la_windows)

# aggregate & organize data
input_data = [[], []]
for instance in synthetic_columbus_features:
    single_feature_vector = combine_feature_vectors(instance)
    input_data[0].append(single_feature_vector)
    input_data[1].append("Columbus")
#for instance in synthetic_dayton_features:
#    single_feature_vector = combine_feature_vectors(instance)
#    input_data[0].append(single_feature_vector)
#    input_data[1].append("Dayton")
for instance in synthetic_wildwood_features:
    single_feature_vector = combine_feature_vectors(instance)
    input_data[0].append(single_feature_vector)
    input_data[1].append("Wildwood")
for instance in synthetic_framingham_features:
    single_feature_vector = combine_feature_vectors(instance)
    input_data[0].append(single_feature_vector)
    input_data[1].append("Framingham")
for instance in synthetic_menomonie_features:
    single_feature_vector = combine_feature_vectors(instance)
    input_data[0].append(single_feature_vector)
    input_data[1].append("Menomonie")
for instance in synthetic_la_features:
    single_feature_vector = combine_feature_vectors(instance)
    input_data[0].append(single_feature_vector)
    input_data[1].append("Los Angeles")

# split the data
X = input_data[0]
print("Instances used in KNN: %d" % len(input_data[0]))
y = input_data[1]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0)

# Fit the model on training data, predict on test data
# For most of the synthetic data we duplicate a trace 40 times, choosing K <= 40 results
# in perfect predictions.
clf = KNeighborsClassifier(n_neighbors=K_VALUE)
clf.fit(X_train, y_train)
prediction = clf.predict(X_test)
print("Prediction: %s\n" % prediction)
print("y_test: %s\n" % y_test)
accuracy = accuracy_score(y_test, prediction)
title = "New Features:%s K=%d Noise=%dms Datapoints=%d Accuracy=%.3f" % (NEW_FEATURES, K_VALUE, NOISE, len(input_data[0]), accuracy)
print("KNN Model Accuracy Score: %s\n" % accuracy)
y_score = clf.predict_proba(X_test)[:, 1]
# y_score = clf.predict(X_test)

fig = px.scatter(
    X_test, x=0, y=1,
    color=y_score,        # or use y_test
    color_continuous_scale='RdBu',
    symbol=y_test,      # assign symbols for each city
    labels={'symbol': 'label', 'color': 'score of <br>first class'},
    title=title
)
fig.update_traces(marker_size=12, marker_line_width=1.5)
fig.update_layout(legend_orientation='h')
fig.show()

client.close()  # disconnect from mongodb
