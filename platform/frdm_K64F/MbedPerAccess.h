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

#ifndef _ARD_PER_ACCESS_H
#define _ARD_PER_ACCESS_H

#include "PerAccess.h"
#include "error.h"

#ifndef MBED
#define MBED                                                   /**< Build for mbed */
#endif

class MbedPerAccess : public PerAccess
{
public:
    virtual uint digitalOut(uint pinNo, uint val);
    virtual uint digitalIn(uint pinNo, uint * val);
    virtual uint analogOut(uint pinNo, uint val);
    virtual uint analogIn(uint pinNo, uint * outVal);
private:


    static const uint _maxDigiOutPins = 25;                    /**< Maximun number of digital out pins */
    static const uint _maxDigiInPins = 25-4;                   /**< Maximum number of digital in pins */
    static const uint _maxAnInPins = 6;                        /**< Maximum number of ADC channels */
    static const uint _maxAnOutVal = 4096;                     /**< Maximum value that can be output by the ADC uint */



};

#endif

