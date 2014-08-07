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
 
/**
*   \brief          Implements the mbed perephiral access interface
*   \author         Navin Bhaskar
*/

/**
 * Implements the peripheral access functionalities
 */

#include "MbedPerAccess.h"
#include "error.h"
#include "mbed.h"

/**
 * Outputs the given logic level at the given pin
 */

uint MbedPerAccess::digitalOut(uint pinNo, uint val)
{
    DigitalOut ports[] = {
                         D0,  D1,  D2,  D3,  D4,  D5,  D6,  D7,  D8,  D9,  D10,  D11,  D12,  D13,  D14,  D15,
                         A0,  A1,  A2,  A3,  A4, A5, LED_RED, LED_GREEN, LED_BLUE
                         };
    if (pinNo > _maxDigiOutPins) {

        return ERR_INVALID_PIN;
    }
    if (val == 0) {
        ports[pinNo] = 0;
    } else {
        ports[pinNo] = 1;
    }
    return ERR_SUCCESS;
}

/**
 * Reads the voltage level at given pin and returns
 * it's logical value.
 */

uint MbedPerAccess::digitalIn(uint pinNo, uint * val)
{
    DigitalIn ports[] = {
                         D0,  D1,  D2,  D3,  D4,  D5,  D6,  D7,  D8,  D9,  D10,  D11,  D12,  D13,  D14,  D15,
                         A0,  A1,  A2,  A3,  A4, A5
                        };
    if (pinNo > _maxDigiInPins) {
        return ERR_INVALID_PIN;
    }


    *val = ports[pinNo];
    return ERR_SUCCESS;
}

/**
 * Outputs the analog value.
 */

uint MbedPerAccess::analogOut(uint pinNo, uint val)
{
    AnalogOut aout(DAC0_OUT);
    if (val > _maxAnOutVal) {
        return ERR_INVALID_ARG;
    }
    /* Only one analog out */
    if (pinNo != 18) {
        return ERR_INVALID_PIN;
    }
    aout = val;
    return ERR_SUCCESS;
}

/**
 * Reads the volatge at the given analog input pin
 * and returns the digital representation of the same
 */

uint MbedPerAccess::analogIn(uint pinNo, uint * outVal)
{
    float val;
    AnalogIn ana_in[] = { A0,  A1,  A2,  A3,  A4, A5 };
    if (pinNo > _maxAnInPins) {
        return ERR_INVALID_PIN;
    }

    val = ana_in[pinNo];
    *outVal = (int)(val*100);
    return ERR_SUCCESS;
}
