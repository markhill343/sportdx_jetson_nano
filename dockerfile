# Use the official NVIDIA Jetson Nano base image
FROM nvcr.io/nvidia/l4t-pytorch:r32.6.1-pth1.9-py3

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3.8-venv \
    python3.8-dev \
    python3-pip \
    libopencv-dev \
    python3-opencv \
    v4l-utils \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python3.8 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Upgrade pip
RUN python3.8 -m pip install --upgrade pip

# Install required Python packages
RUN pip install ultralytics numpy matplotlib flask jupyter

# Copy your application code
COPY . /app
WORKDIR /app

# Expose the ports to access the server
EXPOSE 8080
EXPOSE 8888
# Run the application
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
