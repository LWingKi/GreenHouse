# GreenHouse
All about Hardware setting:<br /> 
1.check all IO pin setting by command "gpio readall"<br /> 
2.check if I2C is successfully connected by command "i2cdetect y -1"<br /> 
3.download pigpio library to use mutiple PWM<br /> 
4.everytime you switch on pi, you have to use command "sudo pigpiod"<br /> 
5.must commond GND  everything (connect the black wire on 5V/GND side to any GND pin on pi)<br /> 
6.You have to make a voltage divider to convert 5V->3.3V to make sensor work. (10K//20K)<br /> 
7.if the outpur devices is on when PWM is in 0% duty cycle, MOSFET boom boom<br /> 
8.the socket needs 12V input voltage, dont give other value, it won't work.
