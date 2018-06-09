# vision-2018
Vision code for the 2018 Sailbot

# Setting up the onboard IMU
`git clone https://github.com/richardstechnotes/RTIMULib2.git`  
`sudo apt install libqt4-dev`
`cd RTIMULib2/Linux`  
`mkdir build`  
`cd build`  
`cmake .. -DBUILD_GL=OFF -DBUILD_DEMOGL=OFF`
`make -j4`
`sudo make install`
`sudo ldconfig`

# Generating an New RTIMULib.ini File
`sudo RTIMULibDemo`
Select IMU
select bus type = SPI bus 3
select IMU type = InvenSense MPU9250
select I2C address type = Standard
