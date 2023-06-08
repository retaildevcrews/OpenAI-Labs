FROM python:3.10.12-bullseye
WORKDIR /home/
COPY . .
RUN apt-get update
RUN apt-get install -y \
    curl \
    gnupg2 \
    jq \
    software-properties-common \
    zsh\
    sudo
ARG USERNAME=python
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
ENV PATH="/home/$USERNAME/.local/bin:$PATH"
RUN python3 -m pip install -r requirements.txt
RUN bash ./setup.sh 
