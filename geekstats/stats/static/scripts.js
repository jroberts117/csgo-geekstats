
                
    document.getElementById("rangeButton").onclick = function() {
        document.getElementById("dateSeasons").style['display'] = "none";
        document.getElementById("dateMatches").style['display'] = "none";
        document.getElementById("dateDates").style['display'] = "inline-block";
        document.getElementById("rangeButton").style['display'] = "none";
        document.getElementById("matchButton").style['display'] = "block";
        document.getElementById("seasonButton").style['display'] = "block";
    };

    document.getElementById("matchButton").onclick = function() {
        document.getElementById("dateSeasons").style['display'] = "none";
        document.getElementById("dateMatches").style['display'] = "inline-block";
        document.getElementById("dateDates").style['display'] = "none";
        document.getElementById("rangeButton").style['display'] = "block";
        document.getElementById("matchButton").style['display'] = "none";
        document.getElementById("seasonButton").style['display'] = "block";
    };

    document.getElementById("seasonButton").onclick = function() {
        document.getElementById("dateSeasons").style['display'] = "inline-block";
        document.getElementById("dateMatches").style['display'] = "none";
        document.getElementById("dateDates").style['display'] = "none";
        document.getElementById("rangeButton").style['display'] = "block";
        document.getElementById("matchButton").style['display'] = "block";
        document.getElementById("seasonButton").style['display'] = "none";
    };

    function showGraph() {
        document.getElementById("graph").style['display'] = "block";
    };
    
    function hideGraph() {
        document.getElementById("graph").style['display'] = "none";
    };
    