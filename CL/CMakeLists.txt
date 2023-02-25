cmake_minimum_required(VERSION 3.24)
project(CL C)

set(CMAKE_C_STANDARD 11)

add_executable(CL main.c array_utils/ArrayUtils.c array_utils/ArrayUtils.h AtCommand.c AtCommand.h AtCommands.c AtReader.c AtReader.h AtResponse.h AtresponseCallback.h AtResponseFunctionPointer.h array_utils/AtResponseArray.c array_utils/AtResponseArray.h NbIoT.c NbIoT.h Param.h ResponseStatusEnum.h SocketStatusEnum.h TimeUtils.c TimeUtils.h AirQMock.c Serial.c string_utils/CharPtrArray.c string_utils/CharPtrArray.h ResponseStatusNames.h AtResponse.c string_utils/AtString.h string_utils/StringArray.c string_utils/StringArray.h string_utils/AtString.c)
