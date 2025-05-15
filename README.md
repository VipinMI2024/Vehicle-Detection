
# Real-Time Vehicle Detection and Counting System

## Project Overview

This project implements a **real-time vehicle detection and counting system** using **Python** and **OpenCV**. The system detects and counts vehicles in motion in a video feed using **MOG2** for background subtraction and contour detection. Vehicles are tracked and counted as they cross a predefined line in the video frame.

## Key Features

* **Real-Time Vehicle Detection**: Detects vehicles in motion from a video stream.
* **Accurate Counting Logic**: Tracks and counts vehicles that cross a defined line in the frame.
* **Bounding Boxes & Live Count Display**: Displays bounding boxes around detected vehicles and updates the vehicle count in real time.
* **Noise Reduction**: Optimized to handle real-world footage with minimal noise and errors.
* **Multi-Scene Compatibility**: Works across various video scenes with different vehicle types.

## Technical Highlights

* **MOG2 Background Subtraction**: Uses **MOG2** to separate foreground (vehicles) from the background.
* **Contour Filtering**: Filters contours based on aspect ratio and bounding box dimensions to accurately identify vehicles.
* **Line-Crossing Logic**: Real-time vehicle counting when vehicles cross a predefined line.
* **Optimized for Real-World Footage**: Includes noise reduction strategies and performance optimizations.

## Installation

To get started with this project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/vehicle-detection.git
cd vehicle-detection
pip install -r requirements.txt
```

### Dependencies:

* **Python 3.x**
* **OpenCV**
* **NumPy**
* **Matplotlib** (for visualizations)

## Usage

1. **Prepare Video Input**: Place the video file you want to analyze in the project directory (or use the provided sample video).

2. **Run the Vehicle Detection Script**:

```bash
python main.py
```

3. **Output**: The script will display a live feed with bounding boxes around detected vehicles and a count of vehicles passing the line.

## Project Structure

```
vehicle-detection/
│
├── main.py            # Main script for vehicle detection and counting
├── utils.py           # Utility functions for contour filtering, background subtraction, etc.
├── config.py          # Configuration file for system parameters (e.g., line position, video source)
├── vehicles.mp4       # Sample traffic video for testing
├── requirements.txt   # List of required dependencies
└── README.md          # Project documentation
```
## Potential Applications

* **Smart City Traffic Monitoring**: Monitor and analyze traffic flows in urban areas.
* **Urban Infrastructure Analytics**: Understand vehicle movements and congestion patterns in city infrastructure.
* **Intelligent Transport Systems (ITS)**: Use real-time vehicle counting for better traffic management and planning.

## Contributing

If you want to contribute to this project, feel free to fork the repository, make improvements, and submit a pull request. Contributions are always welcome!




