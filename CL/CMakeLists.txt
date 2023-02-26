cmake_minimum_required(VERSION 3.24)
project(CL C)

set(CMAKE_C_STANDARD 11)

add_executable(CL main.c array_utils/ArrayUtils.c array_utils/ArrayUtils.h at_commands/AtCommand.c at_commands/AtCommand.h at_commands/AtCommands.c AtReader.c AtReader.h at_responses/AtResponse.h at_responses/AtresponseCallback.h at_responses/AtResponseFunctionPointer.h array_utils/AtResponseArray.h NbIoT.c NbIoT.h at_responses/Param.h at_responses/ResponseStatusEnum.h SocketStatusEnum.h time_utils/TimeUtils.c time_utils/TimeUtils.h AirQMock.c Serial.c string_utils/CharPtrArray.c string_utils/CharPtrArray.h at_responses/ResponseStatusNames.h at_responses/AtResponse.c string_utils/AtString.h string_utils/StringArray.c string_utils/StringArray.h string_utils/AtString.c constants.h)
