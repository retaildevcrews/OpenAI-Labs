## update and install some things we should probably have
echo "post create started" >> $HOME/status

## set up nbscript
nbstripout --install
nbstripout --install --attributes .gitattributes
nbstripout --install --global

echo "post create completed" >> $HOME/status
