#include "AtCommand.h"
#include "AtResponse.h"

static AtResponse ERROR_RESPONSE = {
    .status = STATUS_ERROR,
    .response = {"ERROR"},
    .response_size = 1,
    .wanted = NULL,
    .wanted_size = 0};

static AtCommand *at_read_ati()
{
    AtResponse ati_response = {
        .status = STATUS_OK,
        .response_size = 4,
        .response = {"Quectel_Ltd", "Quectel_BC66NA", "Revision: BC66NBR01A01:<revision>", "OK"},
        .wanted_size = 1,
        .wanted = {{.name = "<revision>", .value = "", .response_row = 2}}};

    AtResponsesArray *expected_responses = create_at_responses_array(2, {ati_response, ERROR_RESPONSE});

    AtCommand *ati = createAtCommand("ATI", "Display Product Identification Information.", expected_responses_size, expected_responses, 1);

    return ati;
}
static AtCommand *at_read_imei()
{
    AtResponse ati_response = {
        .status = STATUS_OK,
        .response_size = 4,
        .response = {"+CGSN:<IMEI>", "OK"},
        .wanted_size = 1,
        .wanted = {{.name = "<IMEI>", .value = "", .response_row = 0}}};

    int expected_responses_size = 2;
    AtResponsesArray *expected_responses = create_at_responses_array(2, {ati_response, ERROR_RESPONSE});

    AtCommand *imei = createAtCommand("AT+CGSN=1", "Display Product Identification Information.", expected_responses_size, expected_responses, 1);

    return imei;
}