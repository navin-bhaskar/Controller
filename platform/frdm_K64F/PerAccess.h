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
 * Defines a abstract class that allows access to the peripherlas
 * on board when implemented completely.
 */

#ifndef _PER_ACCESS_H
#define _PER_ACCESS_H
#include "error.h"
#include <stdint.h>
class PerAccess
{
    public:
    virtual uint digitalOut(uint pinNo, uint val) = 0;
    virtual uint digitalIn(uint pinNo, uint * outVal) = 0;
    virtual uint analogIn(uint pinNo, uint * outVal) = 0;
    virtual uint analogOut(uint pinNo, uint val) = 0;
    
};
#endif
