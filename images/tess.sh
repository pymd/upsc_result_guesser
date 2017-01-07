tesseract eng2.LobsterTwo.exp0.png eng2.LobsterTwo.exp0 nobatch box.train

unicharset_extractor eng2.LobsterTwo.exp0.box

# font name <italic> <bold> <fixed> <serif> <fraktur>
echo "LobsterTwo 0 0 0 0 0" > font_properties

shapeclustering -F font_properties -U unicharset eng2.LobsterTwo.exp0.tr

mftraining -F font_properties -U unicharset -O eng2.unicharset 
    eng2.LobsterTwo.exp0.tr

cntraining eng2.LobsterTwo.exp0.tr


# prefix "relevant" files with our language code
mv inttemp eng2.inttemp
mv normproto eng2.normproto
mv pffmtable eng2.pffmtable
mv shapetable eng2.shapetable
combine_tessdata eng2.

# copy the created eng2.traineddata to the tessdata folder
# so tesseract is able to find it
sudo cp eng2.traineddata /usr/local/share/tessdata/