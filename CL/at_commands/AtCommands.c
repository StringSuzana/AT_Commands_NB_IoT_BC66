#include "AtCommand.h"
#include "../at_responses/AtResponse.h"

static AtResponse ERROR_RESPONSE = {
        .status = STATUS_ERROR,
        .rows_array = {
                .values = {{.text = "ERROR", .length = 5}},
                .size = 1},
        .wanted_params_array = NULL,
        .wanted_params_size = 0
};

static AtCommand at_read_ati()
{
    const AtResponse ati_response = {
            .status = STATUS_OK,
            .rows_array = {
                    .values = {{.text = "Quectel_Ltd", .length = 11},
                               {.text="Quectel_BC66", .length=12},
                               {.text="Revision: <revision>", .length=20},
                               {.text="OK", .length=2}},
                    .size = 4},
            .wanted_params_size = 1,
            .wanted_params_array = {{.name = "<revision>", .value = "", .response_row = 2}}
    };

    AtResponseArray expected_responses = {
            .responses_size = 2,
            .responses = {ati_response, ERROR_RESPONSE}
    };
    const AtCommand ati = {
            .command = "ATI",
            .description = "Display Product Identification Information.",
            .expected_responses_size = 2,
            .expected_responses = expected_responses,
            .max_wait_for_response = 1
    };
    return ati;
}

static AtCommand at_read_imei()
{
    const AtResponse imei_response = {
            .status = STATUS_OK,
            .rows_array = {
                    .values = {{.text = "+CGSN:<IMEI>", .length = 12},
                               {.text="OK", .length=2}},
                    .size = 2},
            .wanted_params_size = 1,
            .wanted_params_array = {{.name = "<IMEI>", .value = "", .response_row = 0}}
    };
    AtResponseArray expected_responses = {
            .responses_size = 2,
            .responses = {imei_response, ERROR_RESPONSE}
    };
    const AtCommand imei = {
            .command = "AT+CGSN=1",
            .description = "Display Product IMEI.",
            .expected_responses_size = 2,
            .expected_responses = expected_responses,
            .max_wait_for_response = 1
    };

    return imei;
}

