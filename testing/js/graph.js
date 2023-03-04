// graph.js contains the graph generation scripts.

// config used for all graphs
var config = {
    responsive: true,
    displaylogo: false
};

// Stanford --------------------------------------------------
// everything pertaining to the outside of the graph
// title, axis names, etc.
var layoutStanford = {
    title: 'Pinging Stanford',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}

// the initialized data
var errorDelayStanford = [0];
var stanfordData = {
    // save x & y from database values
   // x: collectionCount,
    y: errorDelayStanford,
    // each plot has a different name
    // for bar graph this would be 'bar', and so on
    type: 'scatter',
    // legend name
    name: 'Stanford',
    // line properties
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};

// name the data and join as many data sets as you want
var stanfordGraphData = [stanfordData];
Plotly.newPlot('stanfordGraph', stanfordGraphData, layoutStanford, config);
// End Stanford 

// Oregon State -------------------------------------------
var layoutOregon = {
    title: 'Pinging Oregon State',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayOregon = [0];
var oregonData = {
    y: errorDelayOregon,
    type: 'scatter',
    name: 'Oregon',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var oregonGraphData = [oregonData];
Plotly.newPlot('oregonGraph', oregonGraphData, layoutOregon, config);
// End Oregon State

// Auburn -------------------------------------------------
var layoutAuburn = {
    title: 'Pinging Auburn',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayAuburn = [0];
var auburnData = {
    y: errorDelayAuburn,
    type: 'scatter',
    name: 'Auburn',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var auburnGraphData = [auburnData];
Plotly.newPlot('auburnGraph', auburnGraphData, layoutAuburn, config);
// End Auburn

// Alaska -------------------------------------------------
var layoutAlaska = {
    title: 'Pinging Alaska',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayAlaska = [0];
var alaskaData = {
    y: errorDelayAlaska,
    type: 'scatter',
    name: 'Alaska',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var alaskaGraphData = [alaskaData];
Plotly.newPlot('alaskaGraph', alaskaGraphData, layoutAlaska, config);
// End Alaska

// Texas --------------------------------------------------
var layoutTexas = {
    title: 'Pinging Texas',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayTexas = [0];
var texasData = {
    y: errorDelayTexas,
    type: 'scatter',
    name: 'Texas',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var texasGraphData = [texasData];
Plotly.newPlot('texasGraph', texasGraphData, layoutTexas, config);
// End Texas

// Penn State ---------------------------------------------
var layoutPenn = {
    title: 'Pinging Penn State',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayPennState = [0];
var pennStateData = {
    y: errorDelayPennState,
    type: 'scatter',
    name: 'PennState',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var pennStateGraphData = [pennStateData];
Plotly.newPlot('pennStateGraph', pennStateGraphData, layoutPenn, config);
// End Penn State

// North Dakota -------------------------------------------
var layoutDakota = {
    title: 'Pinging North Dakota',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayNorthDakota = [0];
var northDakotaData = {
    y: errorDelayNorthDakota,
    type: 'scatter',
    name: 'NorthDakota',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var northDakotaGraphData = [northDakotaData];
Plotly.newPlot('northDakotaGraph', northDakotaGraphData, layoutDakota, config);
// End North Dakota 

// Colorado -----------------------------------------------
var layoutColorado = {
    title: 'Pinging Colorado',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayColorado = [0];
var coloradoData = {
    y: errorDelayColorado,
    type: 'scatter',
    name: 'Colorado',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var coloradoGraphData = [coloradoData];
Plotly.newPlot('coloradoGraph', coloradoGraphData, layoutColorado, config);
// End Colorado

// Maine --------------------------------------------------
var layoutMaine = {
    title: 'Pinging Maine',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayMaine = [0];
var maineData = {
    y: errorDelayMaine,
    type: 'scatter',
    name: 'Maine',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var maineGraphData = [maineData];
Plotly.newPlot('maineGraph', maineGraphData, layoutMaine, config);
// End Maine

// Wisconsin ----------------------------------------------
var layoutWisconsin = {
    title: 'Pinging Wisconsin',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayWisconsin = [0];
var wisconsinData = {
    y: errorDelayWisconsin,
    type: 'scatter',
    name: 'Wisconsin',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var wisconsinGraphData = [wisconsinData];
Plotly.newPlot('wisconsinGraph', wisconsinGraphData, layoutWisconsin, config);
// End Wisconsin

// Florida ------------------------------------------------
var layoutFlorida = {
    title: 'Pinging Florida',
    xaxis: {
        title: "time"
    },
    yaxis: {
        title: "error delay"
    }
}
var errorDelayFlorida = [0];
var floridaData = {
    y: errorDelayFlorida,
    type: 'scatter',
    name: 'Florida',
    line: {
        dash: 'dot',
        width: 3,
        color: "red"
    }
};
var floridaGraphData = [floridaData];
Plotly.newPlot('floridaGraph', floridaGraphData, layoutFlorida, config);
// End Florida
// updateGraphs updates every server error message graph
function updateGraphs() {

    // stanford graph
    var stanfordID = document.getElementById("StanfordVal")
    Plotly.extendTraces('stanfordGraph', {
        y: [[stanfordID.value]]
    }, [0])

    // Oregon State graph
    var oregonID = document.getElementById("Oregon StateVal")
    Plotly.extendTraces('oregonGraph', {
        y: [[oregonID.value]]
    }, [0])

    // Auburn graph
    var auburnID = document.getElementById("AuburnVal")
    Plotly.extendTraces('auburnGraph', {
        y: [[auburnID.value]]
    }, [0])

    // Alaska graph
    var alaskaID = document.getElementById("AlaskaVal")
    Plotly.extendTraces('alaskaGraph', {
        y: [[alaskaID.value]]
    }, [0])

    // Texas graph
    var texasID = document.getElementById("TexasVal")
    Plotly.extendTraces('texasGraph', {
        y: [[texasID.value]]
    }, [0])

    // Penn State graph
    var pennStateID = document.getElementById("Penn StateVal")
    Plotly.extendTraces('pennStateGraph', {
        y: [[pennStateID.value]]
    }, [0])

    // North Dakota graph
    var northDakotaID = document.getElementById("North DakotaVal")
    Plotly.extendTraces('northDakotaGraph', {
        y: [[northDakotaID.value]]
    }, [0])

    // Colorado graph
    var coloradoID = document.getElementById("ColoradoVal")
    Plotly.extendTraces('coloradoGraph', {
        y: [[coloradoID.value]]
    }, [0])

    // Maine graph
    var maineID = document.getElementById("MaineVal")
    Plotly.extendTraces('maineGraph', {
        y: [[maineID.value]]
    }, [0])

    // Wisconsin graph
    var wisconsinID = document.getElementById("WisconsinVal")
    Plotly.extendTraces('wisconsinGraph', {
        y: [[wisconsinID.value]]
    }, [0])

    // Florida graph
    var floridaID = document.getElementById("FloridaVal")
    Plotly.extendTraces('floridaGraph', {
        y: [[floridaID.value]]
    }, [0])

    // update the graph every 3200ms
    setTimeout(function() {
        updateGraphs();
    },800)
}
updateGraphs()