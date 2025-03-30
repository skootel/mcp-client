# Van Information

## Overview
Skootel maintains a fleet of vans across different regions to support transportation needs. Each van has specific characteristics and operational status.

## Van Properties

- **ID**: Unique identifier for each van
- **Name**: Human-readable name for the van
- **Status**: Current operational status (available, not-avaialble)
- **Slack Channel ID**: Dedicated Slack channel for van communications
- **Capacity**: Maximum number of scooters the van can transport
- **Region**: Geographical region where the van operates (metro, west)
- **Context**: Latest summarized of the health of the van based on the slack communication

## Status Definitions

- **Available**: Van is operational and ready for assignment
- **Not Available**: Van is currently unavailable (may be busy with a trip, in maintenance, or offline)

## Regions

- **Metro**: Serves San Juan, Guaynabo, Arecibo, Bayamon, Cataño, Carolina
- **West**: Serves Mayaguez, Cabo Rojo, Lajas, Parguera, Boqueron, Combate, Isabela, Rincon, Ponce, Añasco, Aguadilla, Guanica

## Operational Rules

1. Vans should only be assigned to trips within their designated region
2. A van can only be assigned if its status is "available". To know if the van is available, you must check the slack channel.  
3. Van cannot transport/rebalance/pickup/drop more scooters than the max capacity
4. The max number of passengers/employees in a van is 2 per van.
4. Metro region vans operate 24 hours
5. West region vans operate 24 hours

## Maintenance Schedule

- Each van undergoes routine maintenance once every two weeks
- Maintenance is logged in Samsara
- Emergency maintenance may be required if issues are reported

## Communication Protocol

- All van-related communications occur in the van's dedicated Slack channel
- Status updates should be posted to the channel immediately
- "Van esta fuera de rotación", means the van is not avaialble
- "Van devuelta a rotación", means the van is available

## Slack integration

- Use the slack tool to check the vans status.
- Store the result of the vans as a json in the file agents/knowledge/van/latest_van_status.json
- Always update the latest_van_status.json file with the result whenever you go to slack and get the latest, make sure you include the date of when you ran it.  The file of current context is reliable for 3.5 hours from when it was run.
