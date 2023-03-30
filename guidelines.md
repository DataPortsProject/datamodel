# DataPorts data models guidelines

This is a set of guidelines for defining new data models.

Before creating a new data model, [explore the existing ones](http://smartdatamodels.org/index.php/list-of-data-models/) to be sure there is already a data model that covers your use case. Recall to use synonyms in your search. E.g. what you might call Public Transport already exists under UrbanMobility. Check [this resource](https://docs.google.com/spreadsheets/d/1vp9rU63R2YXleEg6w2tn1tWx5sb4heY0APK-tHV9e5M/edit#gid=1357587034) to find it out.



## Syntax

+ Use English terms, preferably American English.
+ Use camel case syntax for attribute names (`camelCase`). 
+ Entity type names must start with a Capital letter, for instance, `WasteContainer`.
+ Use names and not verbs for attribute names, ex. `name`, qualifying it when necessary, ex. `totalSpotNumber` or `dateCreated`.
+ Avoid plurals in attribute names, but state clearly when a list of items fits. Ex. `category`. 
+ All first level properties defined in the json schema should have a description attribute.


## Reuse

+ Check for the existence of the same attribute on any of the other models and reuse it, if pertinent. 
+ Have a look at [schema.org](http://schema.org) trying to find a similar term with the same semantics.
+ Try to find common used ontologies or existing standards well accepted by the Community, or by goverments, agencies, etc.
For instance, [Open311](http://www.open311.org/) for civic issue tracking or [Datex II](http://www.datex2.eu/) for transport systems. 


## Data types

+ When possible reuse schema.org data types (`Text`, `Number`, `DateTime`, `StructuredValue`, etc.).
+ Remember that null is not allowed in NGSI-LD and therefore should be avoided as a value.


## Attribute definition

+ Enumerate the allowed values for each attribute. Generally speaking it is a good idea to leave it open for applications to extend the list, provided the new value is not semantically covered by any of the existing ones.

+ State clearly what attributes are mandatory and what are optional. Remember that `null` value should be avoided as it is prohibited in NGSI-LD. The minimum required attributes will make the data models more flexible for other to use them.


+ Internal attributes. In NGSIv2 there are two special attributes created by the system:

    + dateCreated
    + dateModified

+ Similarly in NGSI-LD there are two different:
    + createdAt
    + modifiedAt

those attributes **must NOT be included into the definition of the data model** (spec.md and *schema.*) but they can appear in the payloads of the examples included.



## Numbers

+ If an attribute is a number, include range limits if they exist and are relevant.


## Units

+ Define a default unit for magnitudes. Normally it will be the unit as stated by the international system of units.

+ If a quantity is expressed in a different unit than the default one, use the [unitCode](http://schema.org/unitCode) metadata attribute in NGSI v2. The Property `unitCode` is defined in NGSI-LD and can be used in this case.

+ The list of UN/CEFACT Common Code (3 characters) can be download from this [page](https://www.unece.org/cefact/codesfortrade/codes_index.html). The list is available directly from [here](https://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20.zip).


## Relative values

+ Use values between `0` and `1` for relative quantities, which represent attribute values such as `relativeHumidity`, `precipitationProbability`, etc. 


## Modelling location

+ Use `address` attribute for civic locations as per [schema.org](http://schema.org/address)

+ Use `location` attribute for geographical coordinates. Ideally use GeoJSON for codifying geospatial properties. That works from Orion 1.2 on. If not use, old NGSI version 1 type `coords`.


## Modelling linked data

+ When an entity attribute is used as a link (relationship) to other entities two modelling options are possible:

    + A/ Name the attribute with the prefix `ref` plus the name of the target (linked) entity type. For instance `refStreetlightModel`, represents an attribute which contains a reference to an entity of type `StreetlightModel`. This option has been extensively used by data models initially intended to be used with NGSIv2 . 
    + B/ Name the attribute using a verb (plus optionally an object) such as `hasStop`, `operatedBy`, `hasTrip`, etc. This option is the one advocated by NGSI-LD, as in NGSI-LD URNs are used to identify entities, and NGSI-LD URNs already convey the type of the target entity, for instance `urn:ngsi-ld:gtfs:Stop:S123`.
  
As the current trend is to align with NGSI-LD as much as possible, B option can be considered as the recommended one and A option is to some extent "deprecated".    


## Date Attributes

+ In NGSI v2 attribute type must be `DateTime`.

+ In NGSI-LD, please check the date and time encoding at the [NGSI-LD FAQ](https://github.com/smart-data-models/data-models/blob/master/ngsi-ld_howto.md#airquality-in-ngsi-ld-format).

+ Use the `date` prefix for naming entity attributes representing dates (or complete timestamps). Ex. `dateLastEmptying`. 

+ `dateCreated` in NGSI v2 (`createdAt` in NGSI-LD) must be used to denote the (digital) entity's creation date.

+ `dateModified` in NGSI v2 (`modifiedAt` in NGSI-LD) must be used to denote the (digital) entity's last update date. 

+ `dateCreated` and `dateModified` are special entity attributes provided off-the-shelf by NGSIv2 implementations.
Be careful because they can be different than the actual creation or update date of the real world entity represented by its corresponding digital entity.

+ When necessary define additional attributes to capture precisely all the details about dates.
For instance, to denote the date at which a weather forecast was delivered an attribute named `dateIssued` can be used.
In that particular case just reusing `dateCreated` would be incorrect because the latter would be the creation date of the (digital) entity representing the weather forecast which typically might have a delay. 

## Dynamic attributes

+ Use a metadata attribute named `timestamp` for capturing the last update timestamp of a dynamic attribute. Please note that this is the actual date at which the measured value was obtained (from a sensor, by visual observation, etc.), and that date might be different than the date (metadata attribute named `dateModified` as per NGSI v2) at which the attribute of the digital entity was updated, as typically there might be delay,
specially on IoT networks which deliver data only at specific timeslots.

+ In NGSI-LD use the `observedAt` Property to convey timestamps.

## Internationalization (i18N)

There can be certain entity attributes which content is subject to be internationalized. For instance, the description of a Point of Interest.
The internationalization (i18N) guidelines for the FIWARE Data Models are defined as follows:

+ By default, the value of an attribute subject to be internationalized *should* be expressed in **American English** (`en-US`).
However there can be situations where an English term is not the most common one, for instance, the English
exonym for the city of Livorno (Italy) is a very obscure term, `Leghorn`.
In such situations, the common international name (`Livorno` in our example) in latin script should be used. 

+ There shall always be a term for the original attribute, i.e. it is not allowed to have entity representations which only contain terms associated to language variants. 
+ For each language variant of an internationalized attribute, there shall be an additional entity attribute which name shall be in the form:

`<AttributeName>_<LanguageTag>`  where `AttributeName` is the original attribute name and `LanguageTag` shall be a language tag as mandated by [RFC 5646](https://www.rfc-editor.org/rfc/rfc5646.txt).
W3C provides guidelines on [how to use language tags](https://www.w3.org/International/articles/language-tags/).

[JSON-LD](https://www.w3.org/TR/json-ld/#string-internationalization) can facilitate developers to parse internationalized entity representations, thus Context Producers are encouraged to use JSON-LD (provided that the backing implementations support it).

When parsing plain JSON content, developers should validate that the corresponding JSON terms are actually conveying a language variant of an attribute. For instance, by validating that the term's suffix actually corresponds to a valid language tag and by checking that the corresponding original attribute is contained in the entity.  

Example:

An entity may contain an attribute named `description`. The value of such attribute shall be expressed in American English.
Additionally it might exist an attribute named `description_es` used to convey the value of such a `description` attribute in Spanish.


## Some of the most used attributes

In case of doubt check other existing models! 

+ `name`
+ `alternateName`
+ `description`
+ `serialNumber`
+ `category`
+ `features`
+ `source`
+ `relativeHumidity`
+ `temperature`


## Versioning

çData providers may choose to tag Entities with an additional `schemaVersion` Attribute so that Data Consumers can behave accordingly. This aligns with the https://schema.org/schemaVersion Property definition.

## Definitions' section

The section definitions will be included into the subject-schema.json name of the subject.

## $ref values

Whenever possible they will be absolute references in order to provide the ability to use the data models isolated from the rest of documents