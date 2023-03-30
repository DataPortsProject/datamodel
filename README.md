# DataPorts Data Model

This is the umbrella repository of the DataPorts Data Model. In particular, the repository contains the JSON schemas and documentation of the entity type definitions for maritime transport, as well as [a set of guidelines](https://github.com/DataPortsProject/datamodel/tree/main/guidelines.md) for contributing to the Data Model. In addition, some useful tools are provided in the `utils` folder.


## Entity ID definition guidelines

These guidelines are based on the NGSI-LD standard and, in NGSI v2, they represent a set of good practices to define entity IDs that improves the context queries, subscriptions and discovery actions. According to them, the Entity ID should follow a standard format: `urn:ngsi-ld:<provider>:<entity-type>:<entity-id>`

+ The first four fields are general and represent the data source that provided the entity:

    + `urn` is always set to "urn" and identifies the entity ID as an urn.

    + `ngsi-ld` represents a ngsi-ld entity when setting to "ngsi-ld".

    + `provider` identifies the data provider.

    + `entity-Type` matches the type attribute of the entity.

+ The last field, `entityName`, represents the (particular) identifier of the entity.

Example:

`urn:ngsi-ld:VPF:PortCall:1202206418`


## List of DataPorts entity types
The following table shows the list of the available entity types:


| Vertical | Type | Description |
| -------- | -------- | -------- |
| Cargo     | [Asset](https://github.com/DataPortsProject/datamodel/tree/main/Cargo/Asset/README.md)     | ...     |
| Cargo     | [CargoManifest](https://github.com/DataPortsProject/datamodel/tree/main/Cargo/CargoManifest/README.md)     | ...     |
| Cargo     | [Container](https://github.com/DataPortsProject/datamodel/tree/main/Cargo/Container/README.md)     | ...     |
| Customs     | [Customs](https://github.com/DataPortsProject/datamodel/tree/main/Customs/Customs/README.md)     | Aggregated statitistic of the external commerce recorded in the spanish customs provided by the spanish Tax Agency     |
| Geofencing     | [AssetGeofenceZone](https://github.com/DataPortsProject/datamodel/tree/main/Geofencing/AssetGeofenceZone/README.md)    | Defines a geofencing event that occurred for a given container going in or out a geofence zone at a given date     |
| Land Transport     | [Car](https://github.com/DataPortsProject/datamodel/tree/main/LandTransport/Car/README.md)     | ...     |
| Land Transport     | [Transport](https://github.com/DataPortsProject/datamodel/tree/main/LandTransport/Transport/README.md)     | ...     |
| Land Transport     | [Truck](https://github.com/DataPortsProject/datamodel/tree/main/LandTransport/Truck/README.md)     | ...     |
| Land Transport     | [TruckDriver](https://github.com/DataPortsProject/datamodel/tree/main/LandTransport/TruckDriver/README.md)     | ...     |
| Land Transport     | [Vehicle](https://github.com/DataPortsProject/datamodel/tree/main/LandTransport/Vehicle/README.md)     | Generic class to define any land, sea, or air transport. Of each of these transports, its unique identification, transport type, fuel tank capacity, and register company are saved.     |
| Mobility     | [MobilityData](https://github.com/DataPortsProject/datamodel/tree/main/Mobility/MobilityData/README.md)     | This dataset shows people (passenger) mobility information in Thessaloniki Region. It contains, in an aggreegated level the number of distinct users' movement     |
| Mobility     | [Parking](https://github.com/DataPortsProject/datamodel/tree/main/Mobility/Parking/README.md)     | ...     |
| Mobility     | [TrafficDetection](https://github.com/DataPortsProject/datamodel/tree/main/Mobility/TrafficDetection/README.md)     | ...     |
| Mobility     | [TrafficDetectionDevice](https://github.com/DataPortsProject/datamodel/tree/main/Mobility/TrafficDetectionDevice/README.md)     | ...     |
| Mobility     | [TravelPath](https://github.com/DataPortsProject/datamodel/tree/main/Mobility/TravelPath/README.md)     | ...     |
| Mobility     | [TravelTime](https://github.com/DataPortsProject/datamodel/tree/main/Mobility/TravelTime/README.md)     | ...     |
| Port     | [Port](https://github.com/DataPortsProject/datamodel/tree/main/Port/Port/README.md)     | ...     |
| Port     | [PortZone](https://github.com/DataPortsProject/datamodel/tree/main/Port/PortZone/README.md)     | ...     |
| Port Management  | [Account](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/Account/README.md)    | ...     |
| Port Management  | [AisAntenna](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/AisAntenna/README.md)    | ...     |
| Port Management  | [Booking](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/Booking/README.md)    | ...     |
| Port Management  | [BookingEquipment](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/BookingEquipment/README.md)    | ...     |
| Port Management  | [BookingParty](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/BookingParty/README.md)    | ...     |
| Port Management  | [CommercialShipCall](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/CommercialShipCall/README.md)    | ...     |
| Port Management  | [Consignee](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/Consignee/README.md)    | ...     |
| Port Management  | [Contact](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/Contact/README.md)    | ...     |
| Port Management  | [Event](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/Event/README.md)    | ...     |
| Port Management  | [ExpectedContainerShipCall](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/ExpectedContainerShipCall/README.md)    | ...     |
| Port Management  | [ExpectedCruiseShipCall](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/ExpectedCruiseShipCall/README.md)    | ...     |
| Port Management  | [GateEvent](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/GateEvent/README.md)    | ...     |
| Port Management  | [KeyPerformanceIndicator](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/KeyPerformanceIndicator/README.md)    | A Key Performance Indicator (KPI) is a type of performance measurement. KPIs evaluate the success of an organization or of a particular activity in which it engages  |
| Port Management  | [PortAuthority](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/PortAuthority/README.md)    | ...     |
| Port Management  | [PortCall](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/PortCall/README.md)    | A Port Call is a vessel's visit to the port for a period of time, in order to perform some kind of useful function, like the loading or unloading of goods.     |
| Port Management  | [PortGateEntry](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/PortGateEntry/README.md)    | Data of access through the entry gate. Gate open or closed, gauge, data of the recognition of the vehicle's license plate carried out.     |
| Port Management  | [PortGateExit](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/PortGateExit/README.md)    | Data of the access through the exit gate, Gate open or closed, data of the recognition of the vehicle's license plate carried out.     |
| Port Management  | [Request](https://github.com/DataPortsProject/datamodel/tree/main/PortManagement/Request/README.md)    | ...     |
| Posidonia  | [PosidoniaEvent](https://github.com/DataPortsProject/datamodel/tree/main/Posidonia/PosidoniaEvent/README.md)    | Data Model for the events from Posidonia Port Solution Suite.     |
| Sea Transport     | [Vessel](https://github.com/DataPortsProject/datamodel/tree/main/SeaTransport/Vessel/README.md)     | ...     |
| Tracking     | [Shipment](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/Shipment/README.md)     | It covers all shipment by a certain transport mode (land, sea, or air), and for that transport mode, it indicates the different origin and destination points, and the packaging type (usually a container) that contains the cargo.     |
| Tracking     | [StoredItem](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/StoredItem/README.md)     | Data on logistics warehouses of goods, indicating who is the depositary, and who is the cargo depositor, and also the date on which the action was carried out.     |
| Tracking     | [TrackableEntity](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/TrackableEntity/README.md)     | Base class from which StoredItem, TransportUnit, and Shipment inherit. Describes the asset, indicating name, status, content, number of elements that make it up, weight and volume, and data on the last event that affected it.     |
| Tracking     | [TrackableEvent](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/TrackableEvent/README.md)     | Events that may occur during the shipment of a merchandise through a certain means of transport from an origin to a destination.     |
| Tracking     | [TransportUnit](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/TransportUnit/README.md)     | Identifies the different containers involved in shipments, indicating its type, whether it is full or empty, the owner, and the tare weight.     |


## License

The DataPorts Data Model is licensed under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/). Please refer to the "LICENSE" file for more information.
