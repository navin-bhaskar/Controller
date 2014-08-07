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
*     \file            Trans_layer.cpp
*     \brief           Implements a simple protocol for communication with PC
*     \author          Navin Bhaskar
*/

#include "TransLayer.h"



/**
*     \fn              TransLayer()
*     \brief           constructor for trans layer. Initializes the pointers
*     \param           none
*     \return          none
*/

TransLayer::TransLayer()
{
    _head =_tail = NULL;
}

/**
*     \fn               AddService(call_back_ptr cb, char flag)
*     \brief            Adds a service to the layer. The arguments are passed to
*                       the call back function
*     \param[in]        cb    call back pointer
*     \param[in]        flag  flag to which this packet must respond
*     \return           -1 on error
*/

int TransLayer::AddService(call_back_ptr cb, char flag)
{
    service_ptr temp=_head, mid;

    if (NULL == cb) {
        return -1;
    }

    // we are going to maintain a linked list of services
    mid = (service_ptr)malloc(sizeof(service_list));

    if (NULL == mid) {
        return -1;
    }

    // record entries
    mid->service_function = cb;
    mid->service_flag = flag;
    if (NULL == _head) {
        // first entry ever
        _head = mid;
        mid->next_service = NULL;
    } else {
        // traverese to end of the list for insertion
        while (temp->next_service != NULL) {
            temp = temp->next_service;
        }
        temp->next_service = mid;
        mid->next_service = NULL;
    }
    return 0;
}

/**
*     \fn        SeeServices(void)
*     \brief     Displays all the services available, registered
*     \param     none
*     \return    none
*/

void TransLayer::SeeServices(void)
{
    service_ptr temp = _head;

    while(temp != NULL) {
        Serial.println(temp->service_flag);
        temp = temp->next_service;
    }
}


/**
*    \fn          LookForService(char flag)
*    \brief       This function looks for a service that services given flag
*    \param[in]    flag   flag of the service
*    \return      service ptr containing that has info on service or NULL if service flag
*                 was not found
*/

service_ptr TransLayer::LookForService(char flag)
{
    service_ptr temp = _head;

    while(temp != NULL) {
        if(temp->service_flag == flag) {
            return temp;
        }
        temp = temp->next_service;
    }

    return NULL;
}


/**
*    \fn          MainLoop(void)
*    \brief       This function waits for a flag and then calls appropraite service
*    \param       none
*    \return      none
*    \note        This function never returns has a while(1) at its heart
*/

void TransLayer::MainLoop(Console * cons, PerAccess * per)
{
    char temp, cmd;
    char data_buff[20];
    boolean start_flag = false, data_start_flag=false, packet_formed = false;
    int i =0;


    while(1) {
        if(cons->available() > 0) {
            temp = cons->getCh();
            if(PACKET_START == temp && data_start_flag == false) {
                // start of packet, siganl the starting of packet
                start_flag = true;
                i=0;
            } else if (start_flag == true) {
                cmd = temp;        // this the flag that is going to indicate the service
                start_flag = false;
                data_start_flag = true;
            } else if(data_start_flag == true) {

                if(temp != 0x0d || temp != 0x0a || temp != '\n') {
                    data_buff[i] = temp;
                    i++;
                }
                if(temp == 0x0d || temp == 0x0a) {
                    data_buff[i] = '\0';
                    packet_formed = true;
                    data_start_flag = false;
                }

            }
            if(packet_formed == true) {
                service_ptr ser;
                //SeeServices();
                ser =  LookForService(cmd);
                if(ser != NULL) {
                    ser->service_function(cons, per, data_buff, i);
                }
                packet_formed = false;
            }
        }
    }
}





