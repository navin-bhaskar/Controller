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

#include "Console.h"
#include <WProgram.h>
#include <stdarg.h>
#include "ArdConsole.h"

void ArdConsole::printf(char * fmt, ...)
{
    char tmp[64];
    va_list args;
    va_start(args, fmt);
    vsnprintf(tmp, 64, fmt, args);
    va_end(args);
    Serial.print(tmp);
}

int ArdConsole::available()
{
    return Serial.available();
}

