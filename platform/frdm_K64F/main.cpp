/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 */
#include "mbed.h"
#include "TransLayer.h"
#include "MbedConsole.h"
#include "MbedPerAccess.h"

/**
 * \brief   The main entry point of our application.
 * \author  Navin Bhaskar
 */ 

Serial pc(USBTX, USBRX);
/**
*    \fn          number(char* buff)
*    \brief       This function converts a string into a number.
*    \param[in]   buff    buffer containg string representation of a number (should be decimal representation).
*    \retrun      converted number
*/

int number(char *buff)
{
    int i = strlen(buff);
    int j,temp=0;

    for(j=0; j<i; j++) {
        if(buff[j] >= '0' && buff[j] <= '9') {
            temp = temp*10;
            temp = temp + buff[j] - '0';

        }
    }

    return temp;
}
/**
*  \fn         pin_control(char* buff, int len)
*  \brief      sets or resets a pin
*/
void pin_control(Console * cons, PerAccess * per, char* buff, int len)
{
    uint temp = number(buff);
    uint pinno, pinst;
    uint status;

    if( len < 3) {
        cons->printErr(ERR_INVALID_ARG);
    } else {
        pinst = temp%10;        // LSB is pin state
        pinno = temp/10;        // rest of it is pin number
        status = per->digitalOut(pinno, pinst);
        cons->printErr(status);
    }
}

/**
*    \fn        analog_out(char* buff, int len)
*    \brief     Outputs an anolog voltage on a given PWM channel
*/

void analog_out(Console * cons, PerAccess * per, char* buff, int len)
{
    int temp = number(buff);
    int pinno, pinval;
    uint status;
    if( len < 3) {
        cons->printErr(ERR_INVALID_ARG);
        return ;
    }

    pinno = temp&0xff;        // LSB is pin value
    pinval = temp>>8;           // MSB is pin no
    
    status = per->analogOut(pinno, pinval);
    cons->printErr(status);
}

/**
*  \fn       analog_in(char* buff, int len)
*  \brief    This function reads an analog volatge on a given channel and prints
*            it over on the serial terminal
*/

void analog_in(Console * cons, PerAccess * per, char* buff, int len)
{
    uint adc_val;
    uint ch=number(buff);
    uint status;
    status = per->analogIn(ch, &adc_val);
    if (status == ERR_SUCCESS) {
        cons->printf("%d\n", adc_val);
    }
    cons->printErr(status);
}

/**
*    \fn        read_pin(char* buff, int len)
*    \brief     This function reads digital logic level at a specified pin and prints
*               it over serial port prints 1 if high else it prints 0
*/

void read_pin(Console * cons, PerAccess * per, char* buff, int len)
{
    uint read_val;
    uint pin=number(buff);
    uint status;

    status = per->digitalIn(pin, &read_val);

    if (status == ERR_SUCCESS) {
        cons->printf("%d\n", read_val);
    }
    cons->printErr(status);
}


int main(void)
{
    TransLayer comm_packet;
    MbedConsole cons;
    MbedPerAccess per;

    Console *transCons;
    PerAccess *transPer;

    transCons = &cons;
    transPer = &per;
    

    comm_packet.AddService(pin_control, 'P');
    comm_packet.AddService(analog_out, 'A');
    comm_packet.AddService(analog_in, 'I');
    comm_packet.AddService(read_pin, 'R');
    comm_packet.MainLoop(transCons, transPer);

    while(1);
}
