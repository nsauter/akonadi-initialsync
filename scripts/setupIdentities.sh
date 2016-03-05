#!/bin/bash

#This script copies an existing identites file, and set's it up with a transport from,
#an newly configured identities file.

#This should be correct if the migration has just been executed, keep.
EXISTINGID=~/.kde/share/config/emailidentities
#Adjust this to the source identities to migrate
IDENTITIESTOMIGRATE=~/.kde3/share/config/emailidentities
#This should be correct, keep
TARGETFILE=~/.kde/share/config/emailidentities

#Extract the transport from the existing identities file
TRANSPORT=$(grep Transport $EXISTINGID)

#Copy the source identities file (this may overwrite the EXISTINGID file)
cp $IDENTITIESTOMIGRATE $TARGETFILE

#Setup a valid transport
sed -i "s/Transport=*/$TRANSPORT/g" $TARGETFILE
#Remove fields that are no longer valid (references to folders)
sed -i "/Templates=*/d" $TARGETFILE
sed -i "/Fcc=*/d" $TARGETFILE
sed -i "/Drafts=*/d" $TARGETFILE
sed -i "/Bcc=*/d" $TARGETFILE
#Fix signature if enabled
sed -i "s/Signature Type=inline/Signature Enabled=true\nSignature Type=inline/g" $TARGETFILE
#Default to german dictionary if at default value
sed -i "s/Dictionary=<default>/Dictionary=German (Germany)\nAutocorrection Language=de/g" $TARGETFILE

echo "Identities migrated with transport: $TRANSPORT"
