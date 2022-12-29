                
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

    document.getElementById("allTime").onclick = function() {
        if (document.getElementById("allTime").checked){
            document.getElementById("start").value = "2018-01-01";
            var today = new Date();
            var dd = String(today.getDate()).padStart(2, '0');
            var mm = String(today.getMonth() + 1).padStart(2, '0');
            var yyyy = today.getFullYear();
            today =  yyyy + '-' +  mm + '-' + dd;
            document.getElementById("end").value = today;
            document.getElementById("dateDates").submit();
        }
    };

    document.getElementById("start").onchange = function() {
        document.getElementById("allTime").checked = false;     
    };

    document.getElementById("end").onchange = function() {
        document.getElementById("allTime").checked = false;     
    };

    function showGraph() {
        document.getElementById("graph").style['display'] = "block";
    };
    
    function hideGraph() {
        document.getElementById("graph").style['display'] = "none";
    };


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
            }
        }
        return cookieValue;
        }
