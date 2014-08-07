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
 * Defines all the error codes
 */
 
#ifndef ERROR_H
#define ERROR_H

typedef unsigned int uint;

#define ERR_ERROR                     0             /**< Generic error code */
#define ERR_SUCCESS                   1             /**< Success code */
#define ERR_INVALID_PIN               2             /**< If there is no such physical pin */ 
#define ERR_INVALID_ARG               3             /**< If the passed argument was invalid */

#endif 
