## add local bin directory to path

## update and install some things we should probably have
## setup and install oh-my-zsh
sudo sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
sudo cp -R /root/.oh-my-zsh /home/$USERNAME
sudo cp /root/.zshrc /home/$USERNAME
sudo sed -i -e "s/\/root\/.oh-my-zsh/\/home\/$USERNAME\/.oh-my-zsh/g" /home/$USERNAME/.zshrc
sudo chown -R $USER_UID:$USER_GID /home/$USERNAME/.oh-my-zsh /home/$USERNAME/.zshrc


nbstripout --install
nbstripout --install --attributes .gitattributes
nbstripout --install --global
