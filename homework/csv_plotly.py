from csv import reader
import plotly
import plotly.graph_objs as go


file = open('data/crime.csv')
f = file.read()
line = f.splitlines()
crimes = list(reader(line, delimiter=','))[1:]

for crime in crimes:
    for n in range(len(crime)):
        if crime[n] == '':
            crime[n] = '0'

dataset = {}
for crime in crimes:
    district = crime[4]
    year = int(crime[8])
    shooting = crime[6]
    street = crime[13]
    occured = crime[7]
    code = crime[1]
    number = crime[0]
    if shooting != '0':
        if number in dataset:
            if code in dataset[number]:
                if occured in dataset[number][code]:
                    dataset[number][code][occured]['shooting'] += shooting
                else:
                    dataset[number][code][occured] = {'year': year, 'district': district, 'street': street, 'shooting': shooting}
            else:
                dataset[number][code] = {occured: {'year': year, 'district': district, 'street': street, 'shooting': shooting}}
        else:
            dataset[number] = {code: {occured: {'year': year, 'district': district, 'street': street, 'shooting': shooting}}}

dict_year = {}
dict_distr = {}
dict_street = {}
for nmb in dataset:
    for code in dataset[nmb]:
        for dt in dataset[nmb][code]:
            if dataset[nmb][code][dt]['year'] in dict_year:
                dict_year[dataset[nmb][code][dt]['year']] +=1
            else:
                dict_year[dataset[nmb][code][dt]['year']] = 1
            if dataset[nmb][code][dt]['district'] in dict_distr:
                dict_distr[dataset[nmb][code][dt]['district']] +=1
            else:
                dict_distr[dataset[nmb][code][dt]['district']] = 1
            if dataset[nmb][code][dt]['street'] in dict_street:
                dict_street[dataset[nmb][code][dt]['street']] +=1
            else:
                dict_street[dataset[nmb][code][dt]['street']] = 1

year_gr = go.Scatter(
    x=list(dict_year.keys()),
    y=list(dict_year.values())
)
plotly.offline.plot([year_gr], filename = 'year.html')

street_gr = [go.Bar(
    x = list(dict_street.keys()),
    y = list(dict_street.values()),
    name='Street shooting')]
plotly.offline.plot(street_gr, filename = 'street.html')

distr_gr = go.Pie(labels=list(dict_distr.keys()), values=list(dict_distr.values()))
plotly.offline.plot([distr_gr], filename='districts.html')

file.close()