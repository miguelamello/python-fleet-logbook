# Python Ship Logbook

This is an implementation of a Ship Logbook Service responsible for receiving, collecting, processing and presenting data from "VDR - Vessel Data Recorders" and making it available for further analysis, storage and searchability. The primary goal of a Ship Logbook Service is maintaining a precise log of essential ship instruments readings such as vessel position, speed, heading, engine parameters, rudder movements, communications, alarms and many others. The secondary goal is to provide a way to access this data in a convenient way. For such a task the service provides a "Ingestor Service" to receive data from the VRD and a "Dashboard Service" to provide access to the data though a dashboard. The services also provides a "Disgestor Service" to process the data and make it available for further analysis,  storage or disposal through a API so other services can access it.

## 1) Architecture

The Ship Logbook Service is composed of three main components:

- Ingestor Service
- Dashboard Service
- Disgestor Service

**1.1) Ingestor Service**

The Ingestor Service is responsible for receiving data from the VDRs and storing it in a database. The Ingestor connects to the VDRs through a TCP connection and receives data in the form of NMEA sentences. The Ingestor parses the NMEA sentences and stores the data in a database. As the ship may have issues regarding connectivity, the Ingestor is responsible for keeping trying to connect to the VDRs and each time it connects it will pull all the data that was not received yet. Readings should be saved in a cronomological order, so the Ingestor should be able to detect if readings are out of order, it should be able to detect duplicate entries. Readings should be saved to database in a way that it is easy to query them by time range, by type of reading, by ship, by ship and time range, by ship and type of reading, by ship, type of reading and time range. The Ingestor should be able to detect if the VDR is sending data that is not in the NMEA format and alert developers. 

**1.2) Dashboard Service**

The Dashboard Service is responsible for providing a user graphic interface to access the data. The dashboard should be able to show the data in a way that is easy to understand and navigate. The dashboard should be compatible with desktop and mobile browsers, it also should have a responsive design. Graphic interface should be easy to understand and should be as clear as possible. The dashboard should permit to choose from all available ships, may they be active or inactive. Active meaning when the VDR - Vessel Data Recorder is turned on, and inactive meaning when the VDR is turned off. The dashboard should inform if any expected reading from VDR is not present and alert developers. 

**1.3) Disgestor Service**

The Disgestor Service is responsible to post-processing VDR data and make this data searchable through a GraphQL API. Disgestor should allow direct result data from database, but also asking for data in a asyncronous way. For example, the client may query for a specific data and the Disgestor should return a "pending" status and a "request id". The client may then query for the same data using the "request id" and the Disgestor should return the data if it is ready.

## 2) VDR - Vessel Data Recorder

Ships often have dedicated devices known as VDR, which stands for "Voyage Data Recorders" or "Vessel Data Recorders", that collect and store various vessel data readings. These recorders are specifically designed to capture and record critical data related to the vessel's navigation, operation, and safety.

VDRs are similar to "black boxes" used in aircraft and are mandated by international maritime regulations, such as the International Maritime Organization's (IMO) Safety of Life at Sea (SOLAS) convention. They are typically installed on larger ships, including commercial vessels, passenger ships, and certain types of offshore vessels.

VDRs are equipped with sensors and interfaces to collect data from various onboard systems, including navigation instruments, radar systems, gyrocompasses, GPS receivers, engine and machinery sensors, bridge audio communications, and other relevant equipment. The collected data can include information such as vessel position, speed, heading, engine parameters, rudder movements, communications, and alarms.

In addition to data collection, VDRs often have the capability to record audio and capture images from bridge cameras or other surveillance systems. This comprehensive data recording helps in investigating accidents, understanding vessel operations, analyzing incidents, and improving safety and operational practices.

The recorded data from VDRs is typically stored in a secure and tamper-proof manner, and in the event of an incident, it can be retrieved for analysis and investigation purposes by authorities or ship operators.
However, VDRs can also streamming data in real time to a remote server or allow remote connections to download the data. This is the case of the VDRs used in this project.

**2.1) NMEA - National Marine Electronics Association**

The NMEA 0183 standard defines an electrical interface and data protocol for communications between marine electronic devices such as echo sounder, sonars, anemometer (wind speed and direction), gyrocompass, autopilot, GPS receivers and many other types of instruments. It has been defined by, and is controlled by, the US-based National Marine Electronics Association.

NMEA sentences are standardized data formats used in marine navigation and communication systems. These sentences are ASCII-based and provide a structured way to transmit various types of data between marine electronic devices. NMEA sentences typically start with a dollar sign ($) followed by a two-letter talker ID that identifies the type of device or system providing the data.

Here are a few examples of commonly used NMEA sentences:

**Global Positioning System (GPS) Data:**

**$GPGGA: GPS Fix Data**

<code>$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47</code>

This sentence provides GPS fix information, including time, latitude, longitude, number of satellites in use, altitude, and more.

**$GPRMC: Recommended Minimum Navigation Information**

<code>$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A</code>

This sentence provides essential GPS data such as time, date, latitude, longitude, speed, and course.

**Depth Data:**

**$SDDBT: Depth below transducer**

<code>$SDDBT,12.3,f,3.7,M,2.0,F*0C</code>

This sentence provides depth information measured by the transducer in both feet and meters.

**Wind Data:**

**$WIMWV: Wind Speed and Angle**

<code>$WIMWV,84.3,R,12.4,N,A*0B</code>

This sentence provides wind speed and angle information, including relative (R) or true (T) wind direction.

**AIS (Automatic Identification System) Data:**

**$AIVDM: AIS VHF Data Link Message**

<code>$AIVDM,1,1,,A,13aH52P0tP00l4CNOvNk9An00SGt,0*7E</code>

This sentence contains encoded AIS information transmitted by nearby vessels.

**Compass Data:**

**$HCHDG: Heading, Deviation, and Variation**

<code>$HCHDG,179.8,,,,*14</code>

This sentence provides heading information from a compass, including deviation and variation.


These examples represent just a few of the many NMEA sentence formats available. Different marine devices and systems support various NMEA sentences to facilitate data exchange and interoperability between equipment on board a vessel.

## 3) Ingestor Service - Implementation

The Ingestor Service is implemented in Python 3.11 using the following libraries: 

- signal 
- socket 
- sys, 
- time
- threading
- logging
- dotenv
- mongo_client
- nmea

The service is composed of the following main tasks taht should be implemented:

**3.1) VDR - Vessel Data Recorder remote access**

In a real production ready service, we would have to implement a way to access the VDRs remotely. This could be done in many ways, but the most common way is to use a TCP connection. The VDRs would be configured to open a TCP port and listen for connections. The Ingestor Service would then connect to the VDRs and start receiving data. In this project we will simulate this by using a NMEA datalog file filled with NMEA sentences. The Ingestor Service will read the file and parse the sentences, and deliver each sequence in a 10 seconds interval.

Here is an example of a NMEA datalog file:

```
  $GPGLL,4916.45,N,12311.12,W,2023-06-06T22:54:44,A,*1D
  $GPGLL,4917.60,N,12310.25,W,2023-06-06T22:54:45,A,*45
  $GPGLL,4918.75,N,12309.38,W,2023-06-06T22:54:46,A,*5A
  $GPGLL,4919.90,N,12308.51,W,2023-06-06T22:54:47,A,*6F
  $GPGLL,4921.05,N,12307.64,W,2023-06-06T22:54:48,A,*78
  $GPGLL,4922.20,N,12306.77,W,2023-06-06T22:54:49,A,*89
  $GPGLL,4923.35,N,12305.90,W,2023-06-06T22:54:50,A,*9A
  $GPGLL,4924.50,N,12305.03,W,2023-06-06T22:54:51,A,*AB
  $GPGLL,4925.65,N,12304.16,W,2023-06-06T22:54:52,A,*BC
  $GPGLL,4926.80,N,12303.29,W,2023-06-06T22:54:53,A,*CD
  $GPGLL,4927.95,N,12302.42,W,2023-06-06T22:54:54,A,*DE
  $GPGLL,4929.10,N,12301.55,W,2023-06-06T22:54:55,A,*EF
  $GPGLL,4930.25,N,12300.68,W,2023-06-06T22:54:56,A,*F0
  ...
```

For this demonstration project we will use only `$GPGLL: Geographic Latitude and Longitude` sentences. However, in a real production ready service we would have to implement a way to parse all the NMEA sentences that the VDRs are sending.

**3.2) NMEA sentence parsing**

The Ingestor Service should be able to parse the NMEA sentences in a better fitted format for storage in a database and for further processing. This can be achieved by using the standard Python Type called `dict` that can hold data in many formats. In our specific usecase we will use the `dict` type to hold the data in a key-value format. For example, the `$GPGLL` sentence will be parsed as follows:

```
  {
    'source': '$GPGLL', 
    'latitude': '5019.70N', 
    'longitude': '12223.27W', 
    'utctime': '2023-06-06T22:54:56' 
  }
```

With this format we can easily store the data in a database and also process it in a easy way.

Note: By now we are collecting NMEA sentences from a unique device only. In a real production ready service we would have to implement a way to collect data from multiple devices, and so we would have to add a `device_id` field to the `dict` type. This field would be used to identify the device that sent the data. Maybe wwe could use the serial number of the device as the `device_id`.

**3.3) Database storage of sentences**

The Ingestor Service should be able to store the parsed sentences in a database. For this demonstration project we will use MongoDB as the database. MongoDB is a document-oriented database that stores data in flexible, JSON-like documents, meaning fields can vary from document to document and data structure can be changed over time. The document model maps to the objects in your application code, making data easy to work with. Ad hoc queries, indexing, and real time aggregation provide powerful ways to access and analyze your data. MongoDB is a distributed database at its core, so high availability, horizontal scaling, and geographic distribution are built in and easy to use.

For performance reasons we setted up a `time-series` colletion, and so before saving, some transformation should be made, as follows:

```
{
  'timestamp': '2023-06-06T22:58:03',
  'metadata': {
    'source': '$GPGLL', 
    'latitude': '5019.70N', 
    'longitude': '12223.27W', 
    'utctime': '2023-06-06T22:54:56' 
  }
}
```
Now we can use all the power of MongoDB TimeSeries to query the data in a easy way. The beauty of NoSQL databases like MongoDB is that we can store data in a flexible way, without the need to define a schema in advance. This is very useful when we are dealing with data that is not well defined, as is the case of NMEA sentences. Another advantage on MongoDB is that we can store data in a JSON format, and JSON is a very popular format that is easy to understand and manipulate.

## 4) Disgestor Service - Implementation

The Disgestor Service will is implemented as a GraphQL API using the following libraries: 

  - Flask, which is a lightweight web application framework, designed to make getting 
  started quick and easy, with the ability to scale up to complex applications.

  - Graphene, which is a Python library for building GraphQL schemas/types fast and easily.


We choosed to make the Disgestor Service a GraphQL API because GraphQL is a query language for APIs and a runtime for fulfilling those queries with existing data. GraphQL provides a complete and understandable description of the data as an API, gives clients the power to ask for exactly what they need and nothing more, makes it easier to evolve APIs over time, and enables powerful developer tools.

The service is composed of the following main tasks taht should be implemented:

**4.1) GraphQL Schema**

The GraphQL schema is the core of any GraphQL server implementation. It describes the functionality available to the client applications that connect to it. The schema defines the available API operations and their parameters and return types. It also defines the relationships between the different data types exposed by the API.

## 5) Dashboard Service - Implementation






