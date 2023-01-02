cmake_minimum_required(VERSION 3.24)
project(CL C)

set(CMAKE_C_STANDARD 11)

add_executable(CL main.c ArrayUtils.c ArrayUtils.h AtCommand.c AtCommand.h AtCommands.c AtReader.c AtReader.h AtResponse.h AtresponseCallback.h AtResponseFunctionPointer.h AtResponseArray.c AtResponseArray.h NbIoT.c NbIoT.h Param.h ResponseStatusEnum.h SocketStatusEnum.h TimeUtils.c TimeUtils.h AirQMock.c Serial.c)
