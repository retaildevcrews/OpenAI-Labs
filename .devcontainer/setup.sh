## update and install some things we should probably have
echo "post create started" >> $HOME/status

## set up nbscript in order to clean jupyter notebook files on check in to git
nbstripout --install
nbstripout --install --attributes .gitattributes
nbstripout --install --global
## set git default reconciliation scheme
git config pull.rebase false
## install ohmyzsh
bash -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh) --unattended"

echo "post create completed" >> $HOME/status
