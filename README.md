# RGB Matcher
This is a weekend project that had as goal synchronizing my RGB lighting to the color of my live wallpapers. In the end it was a pretty simple Python script and a long leacture about color theory. Bellow is a demo and a full blog post about this project is coming soon.

![](https://github.com/ransaked1/RGBMatcher/blob/master/RGBMaker.gif)

## Getting Started
Clone the repository and install the prerequisites.

### Prerequisites

Make sure you have python installed:
```
sudo apt-get install python3
```

Install the required packages:
```
pip3 install -r requirements.txt
```
## Usage

Add the script to the windows startup and restart your computer.

## Built With
* [Colorthief](https://pypi.org/project/colorthief/) - color pallete generator from image
* [Watchdog](https://pypi.org/project/watchdog/) - observer to track changes to the wallpaper
* [Govee API](https://pypi.org/project/govee-api-laggat/) - Govee API to control the Govee RGB Lights
* [LogyPi](https://github.com/Logitech/logiPy) - Python wrapper for the Logitech RGB devices
