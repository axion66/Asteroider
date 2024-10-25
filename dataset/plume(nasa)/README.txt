Planetary body limb and plume labels for NASA images

Authors: Marissa Cameron, Gary Doran, and Kiri L. Wagstaff

This data set was compiled to aid in evaluating methods for automated
analysis of images to detect planetary bodies and limbs.  It contains
manually generated labels for 308 NASA images of planets and moons.
The labels annotate the location of the limb (edge) of the body and
plumes emitted by the body, if any.  "Plume" in this context refers to
any bright material emitted from the body, such as icy plumes from
Enceladus or volcanic plumes from Io. 112 of the labeled images
contain plumes.   

== Contents: ==

This data set covers images collected by the following instruments:
1. Cassini Imaging Science Subsystem (ISS)
2. Galileo Solid-State Imaging (SSI)
3. MESSENGER Mercury Dual Imaging System (MDIS)
4. New Horizons Long Rang Reconnaissance Imager (LORRI)

The target bodies include the planet Mercury; Jupiter's moons
Callisto, Europa, Ganymede, and Io; and Saturn's moon Enceladus.

There is a directory for each instrument_target combination:

cassini_iss_enceladus/: Cassini ISS narrow-angle camera observations
of Saturn's moon Enceladus
galileo_ssi_callisto/: Galileo SSI observations of Jupiter's moon Callisto
galileo_ssi_europa/: Galileo SSI observations of Jupiter's moon Europa
galileo_ssi_ganymede/: Galileo SSI observations of Jupiter's moon Ganymede
galileo_ssi_io/: Galileo SSI observations of Jupiter's moon Io
messenger_mdis_mercury/: MESSENGER MDIS narrow-angle and wide-angle
observations of Mercury
new_horizons_lorri_io/: New Horizons LORRI observations of Jupiter's
moon Io

Source images:  The images that are associated with each label file
can be obtained from the Planetary Data System (PDS) at
https://pds-imaging.jpl.nasa.gov/search .
For Cassini ISS, MESSENGER MDIS, and New Horizons LORRI images, search
on the product id from the label filename.  For example, the product
id for 
``lor_0035092814_0x630_sci_label.yml'' is
``lor_0035092814_0x630_sci''.
For Galileo SSI images, the filename does not include the product id.
A list of the source product ids is included in the file named
``galileo_image_ids.txt''.

== Label format: ==

Labels are stored in YAML format.  The limb is annotated as a series of
points marked along the limb such that a least-squares circle fit of
those points provides a model of the body's limb ("points" field).
Plumes, when present, are indicated as one or more angular ranges (in
radians) around the limb within which plume activity is present
("plumes"->"intervals" field).  Angles are specified starting with 0
radians (up) and proceeding clockwise.  The user who generated the
labels is recorded in the "user" field. 

Example (galileo_ssi_io/0085r_label.yml):
Six points define the limb of the body, and there are two areas of
plume activity.  

comment: Points are in (x, y), i.e. (col, row), order.
plumes:
  comment: Intervals in radians
  intervals:
  - [2.8540078295092326, 3.020573420947303]
  - [3.219430581132992, 3.352047930386058]
  user: mcameron
points:
- [123.09103311855094, 322.15933747194225]
- [143.78220150957688, 79.06162214909591]
- [89.23475042871942, 219.0261628709045]
- [256.9650789538681, 407.0275241755675]
- [176.84241267100913, 375.9514805780413]
- [113.07652569773596, 121.72097703075002]
user: mcameron

== Attribution: ==

If you use this data set in your own work, please cite this DOI:
10.5281/zenodo.2556063 .

