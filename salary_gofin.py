import requests # for sending requests
from bs4 import BeautifulSoup # for analysing the responses
import sys # for application arguments


def string_to_salary(string):
# function that changes a string "X XXX,XX zł" to float
    try:
        # cut "zł"
        # remove spaces
        # replace "," to "."
        # convert to float
        return float(string.replace(',','.').replace(" ", "").rstrip('zł'))
    except:
        # when something goes wrong...
        raise Exception("Invalid string structure!")
        # print("Invalid string structure!")
        # return 0


def main(input_gross_list):
# main function that sends a request to the service "https://kalkulatory.gofin.pl/" to calculate Polish salary from gross to net

    for input_gross in input_gross_list:

        # check input
        # is it number?
        if type(input_gross) is str:
            try:
                input_gross = float(input_gross)
            except:
                raise Exception("Invalid entry data - input is not a number!")

        # is it greater than 0?
        if input_gross < 0: raise Exception("Invalid entry data - input must be greater than zero!")

        # url of the site
        engine_url = "https://kalkulatory.gofin.pl/kalkulatory/kalkulator-wynagrodzen-2022"

        # structure of the request
        earnings_data = {
        'description': '',
        'brutto': input_gross,
        'taxReducingAmount': 1,
        'pensionContribution': 1,
        'disabilityContribution': 1,
        'sicknessContribution': '2%2C45%25',
        'healthContribution': '9%25',
        'incomeCosts': 0,
        'taxInstallment': 12
        }

        try:
            # sending a request for data
            response = requests.post(engine_url, data = earnings_data)
        except:
            raise Exception("Connection Error!")

        # cleaning structure of the response
        soup = BeautifulSoup(response.text, features="html.parser")

        # looking for data - results are inside containers: <div class="text-right flex-grow-1 result-value"></div>
        result_data = [item.text for item in soup.select('.result-value')]
        # checking if data is found
        if not len(result_data): raise Exception("Invalid data from the server - output list is empty!")

        # select interesting data and change string to float
        output_gross = string_to_salary(result_data[0]) # first is sent gross salary
        output_net = string_to_salary(result_data[-1]) # the last is calculated net salary

        # check if sent and received data are the same
        if input_gross == output_gross:
            print("For gross salary equal: " + str(input_gross) + " net salary is equal: " + str(output_net)) # print information about the progress
        else:
            raise Exception("Invalid data from the server - output does not match input!")
            # return 0

        yield output_net # return net salary

# when the module is started as the main program
if __name__ == "__main__":

    print(*main(sys.argv[1:]))
