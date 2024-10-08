const cache = require("../utils/cache");
const fetch_servers = require("../utils/fetch_position");

module.exports = get_vehicle_data_json = async (req, res) => {
	if(cache.vehicles_cache.timestamp < Date.now() - 300_000){ //5min

		const temp_vehicles = {};
		const temp_classes = {};
		const temp_object = {
			timestamp: Date.now(),
			sorted_vehicles: [],
			sorted_classes: []
		};

		const servers_array = Object.values(cache.positions) || [];

		await Promise.all(
			servers_array.map(server => 
				server.timestamp < Date.now() - 300000 ? fetch_servers(server) : undefined))

		for (let i = 0; i < servers_array.length; i++) {
			if(servers_array[i].data && servers_array[i].data.players){
				for (let j = 0; j < servers_array[i].data.players.length; j++) {
					const player = servers_array[i].data.players[j];
					// vehicle_name : players[i][4].vehicle_name
					// vehicle_label: players[i][4].vehicle_label,
					// vehicle_class: players[i][4].vehicle_class,
					// vehicle_model: vehicle_model,
					// vehicle_spawn: players[i][4].vehicle_spawn,
					// vehicle_type: players[i][4].vehicle_type,

					//by model
					const vehicle_model = player[4].vehicle_model || -1;
					if(temp_vehicles[vehicle_model] === undefined){
						temp_vehicles[vehicle_model] = [!player[4].vehicle_name || player[4].vehicle_name === "None" ? "None, On Foot" : player[4].vehicle_name, 1];
					}else{
						temp_vehicles[vehicle_model][1]++;
					}

					//by class
					temp_classes[player[4].vehicle_class] = temp_classes[player[4].vehicle_class] === undefined ? 1 : temp_classes[player[4].vehicle_class] + 1;
				}
		  	}
		}

		if(temp_vehicles){
			temp_object.sorted_vehicles = Object.values(temp_vehicles).sort((a,b) => b[1] - a[1])
			temp_object.sorted_classes = Object.entries(temp_classes).sort((a,b) => b[1] - a[1]).map(v=>[parseInt(v[0]), v[1]]);
		}

		Object.assign(cache.vehicles_cache, temp_object);
	}
	
	res.json(cache.vehicles_cache);
}