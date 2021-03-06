# Plastic Pollution in the Ocean
## MDM1 REP3 Project

The simulation is controlled by a **dumping rate** of plastic (in million metric tonnes), 
as well as a distribution of the most abundant plastics and their respective density distributions.

A plastic will float to the ocean floor if its density is greater than the variable **ocean_density** (an average value of the ocean's density),
and float if not.

The metrics collected are then displayed at the top right of the screen, as well as the current year.

These include:

	1. Total Mass: accumalation of the dumping rates over the years (up until 2100)
	2. Floating: percentage of plastics that are floating (i.e. their density is less than ocean_density) 
	3. Sinking: percentage of plastics that are sinking (i.e. their density is greater than ocean_density)
	4. PE: percentage of plastic type PE in ocean
	5. PPA: percentage of plastic type PPA in ocean
	6. PP: percentage of plastic type PP in ocean
	7. PS: percentage of plastic type PS in ocean
	8. OTHERS: percentage of plastics type that is not one of the 4 most abundant types
