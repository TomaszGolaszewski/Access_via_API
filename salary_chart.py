import plotly.express as px # for plot
import pandas as pd # for data structure for plot
import salary_gofin # my module


def main(min, max):
# main function that prepares data and then displays the net(gross) plot
# inputs:
# min - gross minimum wage - bottom limit of the graph - int or float
# max - maximum gross salary - upper limit of the graph - int or float

    # checking if the range is correct
    if min < 0: raise Exception("Invalid entry data - minimum salary must be greater than zero!")
    if max < min: raise Exception("Invalid entry data - minimum salary must be greater than maximum salary!")

    # number of samples minus 1
    no_of_steps = 10

    # calculate step between samples
    step = (max - min) // no_of_steps

    # preparing empty dictionary with data
    dict_with_data = {"Gross salary": [], "Net salary": []}

    # filling the dictionary with data
    # add gross salary
    for gross in range(min, max+1, step):
        dict_with_data["Gross salary"].append(gross)

    # calculate and add net salary
    dict_with_data["Net salary"] = [*salary_gofin.main(dict_with_data["Gross salary"])]

    # preparing Panda's data structure
    df = pd.DataFrame(dict_with_data)
    # preparing plot
    fig = px.line(df, x="Gross salary", y="Net salary", title='net(gross) salary function chart')
    # showing plot
    fig.show()


# when the module is started as the main program
if __name__ == "__main__":
    main(3000, 23000)
