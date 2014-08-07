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


#ifndef __CONSOLE_H
#define __CONSOLE_H
/**
 * \brief    Provides the interfaces for console IO functionality
 */
#include "error.h"
class Console
{
public:
    virtual char getCh() = 0;
    virtual void putCh(char ch) = 0;
    virtual void puts(char *str) = 0;
    virtual void printf(char *fmt, ...) = 0;
    virtual void printErr(uint err) {
        char errMsgs[][20] = {
            "ERROR",
            "SUCCESS",
            "Invalid pin",
            "Invalid arguments"
        };
        if (err > 4) {
            err = 0;
        }
        puts(&errMsgs[err][0]);
        puts("OK");
    }
    virtual int available() = 0;
};

#endif

