var BikesModule = (function(){
	function filterData(data){

	}

	function hasStoredRealTime(station = null) {
		// load the data using the cache module
		var loaded = CacheModule.load("real-time");
		if (loaded == null) {
			return false;
		} 

		return true;

	}

	function saveRealTime(data) {
		CacheModule.save("real-time", data, 60);
	}

    return {
        getStationHistoricalInformation: function(number, day = null, callback = null){
        	var request = window.superagent;	
        	var url = "http://localhost:5000/api/station/" + number;
        	console.log(day);
        	if (day != null){
        		url += "/" + day;
        	}
        	
>>>>>>> 00a60ac1d78d62f1734516ad31bc7cfe6e4632e5
            request.get(url, function(err, response){
				// console.log('Response ok:', response.ok);
				// console.log('Response text:', response.text);
				// need to do more error handling here.
				if (!err){
					var data = JSON.parse(response.text);
<<<<<<< HEAD
					console.log(data);
					// return the station data
				}
			});
        }
=======
					
					// return the station data
					if (callback){
						callback(null, data);
					}

					return data;
				} else {
					if (callback) {
						callback (err, response.text);
						return response.text;
					}

				}

				callback(null, []);
			});
			
        },

        

        getStationInfo: function(address, callback = null) {
        	var request = window.superagent;
        	address = address.replace(/ /g, "-");
        	// ensure its the correct format
        	var url = "http://localhost:5000/api/station-info/" + address;
        	
        	request.get(url, function(err, response){
        		if (!err) {
        			
        			var data = JSON.parse(response.text);
        			if (callback) {
        				callback(null, data);
        			}
        		} else {
        			console.error(response.text);
        		}
				
			});
        },

        getRealTimeData: function(callback) {
        	var request = window.superagent;
        	if (!hasStoredRealTime()) {
        		var url = "http://localhost:5000/api/real-time";
        		console.log("No valid real time data stored. Fetching");
				request.get(url, function(err, response){
					// console.log('Response ok:', response.ok);
					// console.log('Response text:', response.text);
					// need to do more error handling here.
					if (!err) {
						var json = JSON.parse(response.text)
						callback(err, json);
						saveRealTime(json);
					}
					
				});
        	} else {
        		console.log("Valid real time data stored. Loading");
	        	var data = CacheModule.load("real-time");
	        	callback(null, data);
        	
        	}
    	}
>>>>>>> 00a60ac1d78d62f1734516ad31bc7cfe6e4632e5

    }
}())