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
*	\file			trans_layer.h
*	\brief			This file contains functions defines and definations
*				required by trans_layer.c
*	\author			Navin Bhaskar
*/


#ifndef __TRANS_LAYER_H
#define __TRANS_LAYER_H

//#include <string>
#include <WProgram.h>
#include <stdlib.h>
#include "Console.h"
#include "PerAccess.h"

typedef void(* call_back_ptr)(Console * cons, PerAccess * per, char*, int );		/**< typedef for callback function pointer for protocol packets*/

typedef struct service_list* service_ptr;          /**< pointer to next service */

struct service_list {                             /**< Struct for holding service list */
    //char* service_name;                           /**< pointer to the name of the service */
    call_back_ptr service_function;                 /**< call back function pointer */
    char service_flag;                              /**< Packet service flag for which this service responds*/
    service_ptr next_service;
};


#define		PACKET_START		'S'            /**< Start of packet indicator */
#define		QUERY_ADC_DATA		'A'            /**< Control pcaket for quering ADC data */
#define		SET_LCD_DATA	        'L'            /**< To transmit string to be displayed on LCD */
#define 	PACKET_ACK		'V'            /**< Acknowledgement flag */
#define		PACKET_NACK		'N'            /**< Negative acknowledgement */
#define         PACKET_DAT              'D'            /**< Data follows after length field */
#define         PACKET_CMD              'C'            /**< Command follows this field */

#define         PIN_OP                  'P'            /**< Flag indicating pin operations */

class TransLayer
{
private:
    service_ptr _head, _tail;
public:
    TransLayer();
    int AddService(call_back_ptr, char flag);
    void MainLoop(Console *, PerAccess *);
    void SeeServices(void);
    service_ptr LookForService(char flag);
};

#define    PRINT_OK    Serial.println(" OK");          /**< A framing method */

#endif

