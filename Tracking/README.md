# Tracking


### List of data models

The following entity types are available:
- [Shipment](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/Shipment/README.md): It covers all shipment by a certain transport mode (land, sea, or air), and for that transport mode, it indicates the different origin and destination points, and the packaging type (usually a container) that contains the cargo.
- [StoredItem](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/StoredItem/README.md): Data of the interactions with deposits, indicating who is the depositary, and who is the cargo depositor, and also the date on which the action was carried out.
- [TrackableEntity](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/TrackableEntity/README.md): Base class from which transportUnit, storedItem, and Shipment inherit. Describes the asset, indicating name, status, content, number of elements that make it up, weight and volume, and data on the last event that affected it.
- [TrackableEvent](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/TrackableEvent/README.md): Identifies an event.
- [TransportUnit](https://github.com/DataPortsProject/datamodel/tree/main/Tracking/TransportUnit/README.md): Identifies the different containers involved in shipments, indicating its type, whether it is full or empty, the owner, and the tare weight.



### Contributors

VPF



